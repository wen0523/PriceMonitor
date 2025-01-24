from datetime import datetime, timezone, timedelta

def parseTime(zone, timeFrame):
    try:
        zone = int(zone)
        utcTime = datetime.now(timezone.utc)
        timeZone = timezone(timedelta(hours=zone))
        localTime = utcTime.astimezone(timeZone)

        since = int(utcTime.timestamp() * 1000 - parseTimeframe(timeFrame))  # 转换为毫秒级时间戳，用于 API 请求
        return {
            'since':since,
            'localTime':localTime
        }
    except TypeError as e:
        print(e)

def parseTimeframe(timeframe):
    if timeframe.endswith("m"):
        return int(timeframe[:-1]) * 60 * 1000
    elif timeframe.endswith("h"):
        return int(timeframe[:-1]) * 60 * 60 * 1000
    elif timeframe.endswith("d"):
        return int(timeframe[:-1]) * 1440 * 60 * 1000
    else:
        raise ValueError("Invalid timeframe format. Use 'Xm', 'Xh', or 'Xd'.")
