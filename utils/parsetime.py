from datetime import datetime, timezone, timedelta

def parseTime(zone, timeFrame):
    try:
        zone = int(zone)
        utcTime = datetime.now(timezone.utc)
        zoneTime = utcTime + timedelta(hours=zone)
        localTime = zoneTime.strftime("%Y-%m-%d %H:%M")

        since = getSince(localTime)

        # Convert to millisecond timestamp for use in API requests
        sinceCurrent = int((since - 60) * 1000)
        sinceBefore = int(since * 1000 - parseTimeframe(timeFrame))
        return {
            'sinceCurrent':sinceCurrent,
            'sinceBefore':sinceBefore,
            'localTime':localTime
        }
    except TypeError as e:
        print(e)

# Parse 'Timeframe' into milliseconds
def parseTimeframe(timeframe):
    if timeframe.endswith("m"):
        return int(timeframe[:-1]) * 60 * 1000
    elif timeframe.endswith("h"):
        return int(timeframe[:-1]) * 60 * 60 * 1000
    elif timeframe.endswith("d"):
        return int(timeframe[:-1]) * 1440 * 60 * 1000
    else:
        raise ValueError("Invalid timeframe format. Use 'Xm', 'Xh', or 'Xd'.")

def getSince(localTime):
    time_format = "%Y-%m-%d %H:%M"
    time = datetime.strptime(localTime, time_format)
    
    return int(time.timestamp())