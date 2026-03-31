#!/bin/sh /etc/rc.common

START=99

SCRIPT="/lib/uid_manager.py"
PYTHON="/usr/bin/python"
LOG="/tmp/uid_manager.log"
FLAG="/tmp/uid_manager_done"

# ==============================
# 콘솔 자동 감지
# ==============================
get_console_tty() {
    for item in $(cat /proc/cmdline); do
        case "$item" in
            console=*)
                CONS=${item#console=}
                CONS=${CONS%%,*}
                echo "/dev/$CONS"
                return
                ;;
        esac
    done

    # fallback
    for dev in /dev/ttyS0 /dev/ttymxc0 /dev/ttyAMA0; do
        [ -c "$dev" ] && { echo "$dev"; return; }
    done

    echo "/dev/ttyS0"
}

TTY=$(get_console_tty)

start() {

    # ==============================
    # 1회 실행 보장
    # ==============================
    if [ -f "$FLAG" ]; then
        echo "[INFO] already executed, skip" >> $LOG
        logger "[UID] already executed"
        return 0
    fi

    echo "[START] $(date)" >> $LOG
    logger "[UID] init script start"
    echo "[INFO] console: $TTY" >> $LOG

    # ==============================
    # 파일 체크
    # ==============================
    [ -f "$SCRIPT" ] || {
        echo "[ERROR] script not found" >> $LOG
        logger "[UID] script not found"
        return 1
    }

    [ -x "$PYTHON" ] || {
        echo "[ERROR] python not found" >> $LOG
        logger "[UID] python not found"
        return 1
    }

    # ==============================
    # tty 생성 대기
    # ==============================
    echo "[INFO] waiting for tty..." >> $LOG

    COUNT=0
    while [ $COUNT -lt 30 ]; do
        [ -c "$TTY" ] && break
        sleep 1
        COUNT=$((COUNT + 1))
    done

    if [ ! -c "$TTY" ]; then
        echo "[ERROR] tty not available: $TTY" >> $LOG
        logger "[UID] tty not available"
        return 1
    fi

    # ==============================
    #  getty 제거 (핵심)
    # ==============================
    echo "[INFO] killing getty on $TTY..." >> $LOG

    PID=$(ps | grep "[g]etty.*$(basename $TTY)" | awk '{print $1}')

    if [ -n "$PID" ]; then
        kill -9 $PID
        echo "[INFO] getty killed pid=$PID" >> $LOG
        logger "[UID] getty killed"
        sleep 1
    else
        echo "[INFO] no getty found" >> $LOG
    fi

    # ==============================
    # tty 초기화 (입력 안정화)
    # ==============================
    stty -F "$TTY" 115200 sane -echo

    # ==============================
    # 콘솔 깨우기
    # ==============================
    echo "" > "$TTY"
    sleep 1

    echo "[INFO] bind to $TTY" >> $LOG
    logger "[UID] attach $TTY"

    # ==============================
    # tty 바인딩
    # ==============================
    exec < "$TTY" > "$TTY" 2>&1

    echo "[INFO] serial connected $(date)"
    echo "===== UID MANAGER START ====="

    # ==============================
    # Python 실행
    # ==============================
    $PYTHON $SCRIPT
    RET=$?

    echo "===== UID MANAGER END ($RET) ====="

    echo "[END] $(date) ret=$RET" >> $LOG
    logger "[UID] finished ret=$RET"

    # ==============================
    # 실행 완료 표시
    # ==============================
    touch "$FLAG"

    return $RET
}
