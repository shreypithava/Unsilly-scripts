def modify_subtitles(r_file, w_file, secs=5):
    if secs > 59:
        return
    with open(r_file, 'r') as r, open(w_file, 'w') as w:
        for line in r.readlines():
            if '-->' in line:
                added = [add_seconds(line.split(' --> ')[0], secs),
                         add_seconds(line.split(' --> ')[1], secs) + '\n']
                print(' --> '.join(added), end='', file=w)
            else:
                print(line, end='', file=w)


def add_seconds(time, secs):
    t_hour, t_min, t_sec = time.split(':')
    m_sec = int(''.join(t_sec.split(','))) + secs * 1000
    if m_sec > 59999:
        m_sec = str(int(m_sec) - 60000).zfill(5)
        f_min = str(int(t_min) + 1).zfill(2)
        if int(f_min) > 59:
            f_min = '00'
            t_hour = str(int(t_hour) + 1).zfill(2)
        time = [t_hour, f_min, m_sec[:2] + ',' + m_sec[2:]]
    else:
        m_sec = str(int(m_sec)).zfill(5)
        time = [t_hour, t_min, m_sec[:2] + ',' + m_sec[2:]]
    return ':'.join(time)


seconds = 1  # change seconds here
modify_subtitles('origin_file', 'new_empty_file', seconds)
