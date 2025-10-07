import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import csv
import re
import os, glob
from typing import List, Tuple, Dict, Set, Optional
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta

DAY_ALIASES = {
    'monday':'MON','mon':'MON','MON':'MON',
    'tuesday':'TUE','tue':'TUE','tues':'TUE','TUE':'TUE',
    'wednesday':'WED','wed':'WED','WED':'WED',
    'thursday':'THU','thu':'THU','thur':'THU','thurs':'THU','THU':'THU',
    'friday':'FRI','fri':'FRI','FRI':'FRI',
    'saturday':'SAT','sat':'SAT','SAT':'SAT',
    'sunday':'SUN','sun':'SUN','SUN':'SUN',
    # 中文
    '周一':'MON','星期一':'MON',
    '周二':'TUE','星期二':'TUE',
    '周三':'WED','星期三':'WED',
    '周四':'THU','星期四':'THU',
    '周五':'FRI','星期五':'FRI',
    '周六':'SAT','星期六':'SAT',
    '周日':'SUN','星期日':'SUN','周天':'SUN',
}

# Dummy implementations – replace these with your real functions
def norm_day(s: str) -> str:
    if not s:
        return ''
    s = str(s).strip()
    return DAY_ALIASES.get(s, DAY_ALIASES.get(s.lower(), s.upper()[:3]))

TIME_12 = re.compile(r'^\s*(\d{1,2}):(\d{1,2})\s*([APap][Mm])\s*$')
TIME_24 = re.compile(r'^\s*(\d{1,2}):(\d{1,2})\s*$')
def to_24h(s: str) -> str:
    if not s or pd.isna(s):
        return ''
    s = str(s).strip()
    m = TIME_12.match(s)
    if m:
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3).upper()
        if ap == 'AM':
            if h == 12: h = 0
        else:
            if h != 12: h += 12
        return f"{h:02d}:{mi:02d}"
    m = TIME_24.match(s)
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        return f"{h:02d}:{mi:02d}"
    return s

KNOWN_TAGS = ['Forex', 'Gold', 'Indices', 'Oil']

def parse_compair_tags(cell: str) -> Set[str]:
    if cell is None:
        return set()
    s = str(cell).strip()
    if not s:
        return set()
    parts = [p.strip() for p in s.split(',') if p.strip()]
    out = set()
    for p in parts:
        for k in KNOWN_TAGS:
            if p.lower() == k.lower():
                out.add(k)
                break
    return out


def tags_from_profile_name(profile_name: str) -> Set[str]:
    name = (profile_name or '').lower()
    tags = set()
    for k in KNOWN_TAGS:
        if k.lower() in name:
            tags.add(k)
    return tags if tags else set(['_UNKNOWN'])

def pick_key_from_columns(columns, candidates):
    """Find the best matching column from candidates"""
    low = {col.lower(): col for col in columns}
    for cand in candidates:
        if cand.lower() in low:
            return low[cand.lower()]
    return ''  # Default if none match

def is_applicable(profile_tags: Set[str], compair_tags: Set[str]) -> bool:
    if not compair_tags:
        return True
    return bool(profile_tags & compair_tags)


T_BLOCK_SPLIT = re.compile(r'(?=T\d+\s*=\s*)')
T_LABEL_RE = re.compile(r'^(T\d+\s*=\s*[^,;]*[;,]?)', re.IGNORECASE)
IGNORE_PREFIX_RE = re.compile(r'^T\d+\s*=\s*[^,;]*[;,]?\s*', re.IGNORECASE)

def parse_one_tblock_with_label(block: str) -> List[Tuple[str, str, str, str]]:
    """
    返回 [(DAY, START, END, TLABEL)]，例如 TLABEL='T1=0:200;'
    """
    if not block:
        return []
    # 取 T 前缀（保留原样）
    m = T_LABEL_RE.match(block.strip())
    tlabel = m.group(1).strip() if m else ''

    b = IGNORE_PREFIX_RE.sub('', block.strip())  # 去掉前缀再切 token
    tokens = [t.strip() for t in b.split(',') if t.strip()]
    out = []
    i = 0
    while i + 3 < len(tokens):
        d1, t1, d2, t2 = tokens[i], tokens[i+1], tokens[i+2], tokens[i+3]
        D1, D2 = norm_day(d1), norm_day(d2)
        T1, T2 = to_24h(t1), to_24h(t2)
        if D1 and D2 and T1 and T2:
            if not (D1 == 'FRI' and D2 == 'MON'):  # 忽略 Friday→Monday
                out.append((D1, T1, T2, tlabel))
        i += 4
    return out

def parse_sessions_all_with_label(text: str) -> List[Tuple[str, str, str, str]]:
    if not text:
        return []
    blocks = [b for b in T_BLOCK_SPLIT.split(str(text)) if b.strip()]
    segs = []
    for b in blocks:
        segs.extend(parse_one_tblock_with_label(b))
    return segs

def segments_without_label(segs_with_label: List[Tuple[str,str,str,str]]) -> Set[Tuple[str,str,str]]:
    return set((d,s,e) for (d,s,e,_) in segs_with_label)

def covers(day: str, s_exp: str, e_exp: str, segs_set: Set[Tuple[str, str, str]]) -> bool:
    s_exp_m, e_exp_m = _mm(s_exp), _mm(e_exp)
    for (d, s_act, e_act) in segs_set:
        if d != day:
            continue
        if _mm(s_act) <= s_exp_m and _mm(e_act) >= e_exp_m:
            return True
    return False

def covering_tlabel(day: str, s_exp: str, e_exp: str, segs_with_label: List[Tuple[str,str,str,str]]) -> str:
    s_exp_m, e_exp_m = _mm(s_exp), _mm(e_exp)
    for (d, s_act, e_act, tlabel) in segs_with_label:
        if d != day:
            continue
        if _mm(s_act) <= s_exp_m and _mm(e_act) >= e_exp_m:
            return tlabel
    return ''

def export_covers_any(day: str, s_act: str, e_act: str, compairs_applicable: List[Tuple[str,str,str]]) -> bool:
    s_a, e_a = _mm(s_act), _mm(e_act)
    for (d, s_c, e_c) in compairs_applicable:
        if d != day:
            continue
        if s_a <= _mm(s_c) and e_a >= _mm(e_c):
            return True
    return False
# def _mm(t: str) -> int:
#     print(t)
#     h, m , s= t.split(':')
#     return int(h)*60 + int(m)

def _mm(s: str) -> str:

    s = str(s).strip()
    
    # Handle HH:MM:SS directly
    if len(s.split(':')) == 3:
        print("normal time",s)
        h, m, _ = s.split(':')
        return f"{int(h):02d}:{int(m):02d}"
    else:
        print("abnormal time",s)
    m = TIME_12.match(s)
    if m:
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3).upper()
        if ap == 'AM':
            if h == 12: h = 0
        else:
            if h != 12: h += 12
        return f"{h:02d}:{mi:02d}"
    
    m = TIME_24.match(s)
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        return f"{h:02d}:{mi:02d}"
    
    return s
def save_to_excel(rows_out, out_xlsx):
    wb = Workbook()
    ws = wb.active
    ws.title = "Match Report"

    headers = ['Profile','Type','Day','Start','End','Status','TLabel']
    ws.append(headers)

    fill_green  = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # ✔
    fill_red    = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # ✖
    fill_gray   = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")  # NORMAL
    fill_yellow = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")  # N/A

    last_profile = None
    for row in rows_out:
        profile = row[0]
        if last_profile is not None and profile != last_profile:
            ws.append([''] * len(headers))  # 新的 profile 空一行
        ws.append(row)

        status_cell = ws.cell(row=ws.max_row, column=6)  # 第6列 Status
        val = str(row[5]).strip().upper()
        if val in ('✔', '√'):
            status_cell.fill = fill_green
        elif val in ('✖', 'X'):
            status_cell.fill = fill_red
        elif val == 'NORMAL':
            status_cell.fill = fill_gray
        elif val == 'N/A':
            status_cell.fill = fill_yellow

        last_profile = profile

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:G{ws.max_row}"

    widths = [46, 10, 8, 10, 10, 12, 18]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    wb.save(out_xlsx)
uploaded_file = st.file_uploader("Upload阶梯式杠杆Symbol筛选模板",key="compair")
rows=[]
if uploaded_file is not None:
    f1_dataframe = pd.read_excel(uploaded_file,sheet_name="Market News_for_admin")
    # f1_dataframe=f1_dataframe.iloc[:, 5:9]
    # f1_dataframe.rename(columns={f1_dataframe.columns[2]: 'Day'}, inplace=True)
    # st.dataframe(f1_dataframe)
    f1_dataframe=f1_dataframe.iloc[:, 0:4]
        
    f1_dataframe['Time_DT'] = f1_dataframe['Time (GMT+3)'].apply(
    lambda t: datetime.combine(datetime.today(), t)
    )

    # Now perform the timedelta operations
    f1_dataframe['-15 分钟'] = f1_dataframe['Time_DT'] - pd.Timedelta(minutes=15)
    f1_dataframe['+5 分钟'] = f1_dataframe['Time_DT'] + pd.Timedelta(minutes=5)

    # (Optional) If you only want the time part back:
    f1_dataframe['-15 分钟'] = f1_dataframe['-15 分钟'].dt.time
    f1_dataframe['+5 分钟'] = f1_dataframe['+5 分钟'].dt.time

    # (Optional) Drop the temporary datetime column
    f1_dataframe.drop(columns=['Time_DT'], inplace=True)

    f1_dataframe['Day'] = f1_dataframe['Date'].dt.day_name().str[:3].str.upper()
    # f1_dataframe.rename(columns={f1_dataframe.columns[2]: 'Day'}, inplace=True)

    for idx, row in f1_dataframe.iterrows():
        if row['Currency/Country'].strip() == "OIL":
            f1_dataframe.at[idx, 'Profile'] = "Oil"
        elif row['Currency/Country'].strip() == "USD":
            f1_dataframe.at[idx, 'Profile'] = "Forex,Gold,Indices"
        else:
            f1_dataframe.at[idx, 'Profile'] = "Forex"
    f1_dataframe=f1_dataframe.iloc[:, 4:9]
    st.dataframe(f1_dataframe)

    for _, row in f1_dataframe.iterrows():
        if pd.isna(row['-15 分钟']) or pd.isna(row['+5 分钟']) or pd.isna(row['Day']):
            continue

        tags = parse_compair_tags(row['Profile']) if row['Profile'] else set()
        start = to_24h(row['-15 分钟'])  # Update to format as HH:MM
        end = to_24h(row['+5 分钟'])
        day = norm_day(row['Day'])

        rows.append((day, start, end, tags))

    # print(rows)


uploaded_symbol_profiles_file = st.file_uploader("Upload Symbol Profiles",key="symbol_profiles")
if uploaded_symbol_profiles_file is not None:

    f2_dataframe = pd.read_excel(uploaded_symbol_profiles_file)
    rows_out = []    
    for _, row in f2_dataframe.iterrows():
        if '[News + General]' not in row["ProfileStrategyName"]:
            continue
        p_tags = tags_from_profile_name(row["ProfileStrategyName"])
        compairs_applicable = [(d, s, e) for (d, s, e, tags) in rows
                               if is_applicable(p_tags, tags)]
        # print(compairs_applicable)
        segs_with_label = parse_sessions_all_with_label(row["Sessions"])
        seg_set = segments_without_label(segs_with_label)

        for (d, s, e, tags) in rows:
            if is_applicable(p_tags, tags):
                ok = covers(d, s, e, seg_set)
                if ok:
                    tlabel = covering_tlabel(d, s, e, segs_with_label)
                    status = '✔'
                else:
                    tlabel = ''
                    status = '✖'
            else:
                status = 'NORMAL'
                tlabel = ''
            rows_out.append([row["ProfileStrategyName"], 'EXPECT', d, s, e, status, tlabel])

        # EXTRA：只看适用集合；TLabel = 该导出段的标签
        for (d, s, e, tlabel) in sorted(segs_with_label):
            if not export_covers_any(d, s, e, compairs_applicable):
                rows_out.append([row["ProfileStrategyName"], 'EXTRA', d, s, e, 'N/A', tlabel])
    # print(rows_out)
    headers = ['Profile', 'Type', 'Day', 'Start', 'End', 'Status', 'TLabel']
    output = BytesIO()

    excel_bytes = save_to_excel(rows_out,output)
    excel_bytes = output.getvalue()

    st.download_button(
        label="📥 下载报告 (Excel)",
        data=excel_bytes,
        file_name="report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )