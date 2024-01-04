from machine import Pin, UART

import utime, time

gpsModule = UART(1)
# per the ublox manual for Serial Port Output: "9600 Baud, 8 bits, no parity bit, 1 stop bit"
# FYI: 9600 worked in my testing, but u-blox and micropython esp32 says it supports 115200,but i tried taht and it didn't work (may require sending some message to gps to adjust)
gpsModule.init(baudrate=9600, tx=4, rx=36, bits=8, parity=None, stop=1)

print('GPS module configured as:', gpsModule)

buff = bytearray(255)

def debug(msg: str) -> None:
    print(msg)

def read():
    '''
    Parses a line from the GPS.
    If the line is a valid NMEA line it returns it as a set of fields in a list.
    If the line is invalid, an empty list is returned.    
    '''
    # to be a valid message the message must meet the following criteria:
    #  - Begin with a $
    #  - End with a CRLF sequence
    #  - The two hexedecimal digits preceeding the CRLF is a checksum. Those two characters are preceeded by a *.
    #    The checksum is the XOR of all characters between the $ and the *
    bits = gpsModule.readline()
    if bits == None:
        debug('GPS returned nothing.')
        return []
    length = len(bits)
    if length < len('$GP...*hh..'):
        debug(f'GPS returned line with too short of a length ({length}).Full line was: {bits}')
        return []
    if bits[0:1] != b'$':
        debug(f'GPS message did not begin with "$" (was "{bits[0]}"). Ignoring.')
        return []
    # ends in CRLF preceeded by two characteers representing a hex number: https://en.wikipedia.org/wiki/NMEA_0183
    checksumbytes = bits[-4:-2]
    # it is two bytes. Each byte represents a hexedecimal value:
    checksum = 16 * from_hex(checksumbytes[0]) + from_hex(checksumbytes[1])
    # The checksum is the bitwise exclusive OR of ASCII codes of all characters between the $ and *, not inclusive.
    check_bytes = bits[1:-5]
    parity = 0
    for b in check_bytes:
        parity ^= b
    if checksum != parity:
        if bits[0:6] != b'$GPTXT' or check_bytes.find(b'ANTSUPERV') < 0:
            # some of these GPTXT lines with "ANTSUPERV" consistently fail checksum while other lines pass it
            debug(f'GPS line failed checksum. Expected {hex(checksum)} calculated {hex(parity)}. Full line was: {bits}')
        return []
    #debug('checksum passed')
    return bits.split(b',')

def parse_time(hhmmss_ss: bytes) -> str:
    '''
    parses the gps time into an ISO time field
    '''
    hh = hhmmss_ss[0:2].decode()
    mm = hhmmss_ss[2:4].decode()
    ss = hhmmss_ss[4:].decode()
    return f'{hh}:{mm}:{ss}'

def parse_date(ddmmyy: bytes) -> str:
    '''
    parses the gps date into an ISO date field
    '''
    dd = ddmmyy[0:2].decode()
    mm = ddmmyy[2:4].decode()
    yy = ddmmyy[4:].decode()
    return f'{yy}-{mm}-{dd}'

def get_fix(gpsModule):
    # try for 8 seconds to get a GPS Fixed Position
    max_timeout = time.time() + 5
    
    while True:
        # note buff is of type bytes:
        fields = read()
        msg = fields[0] if len(fields) > 0 else b''
        if msg == b'':
            # we ignore these messages as they failed checksum or were invalid
            pass
        elif msg == b'$GPGGA':
            # GGA: Global positioning system fix data message:
            print(f'GPX Fix Received: {fields}')
            # Current Time UTC:
            utc = parse_time(fields[1])
            # Latitude, Degress + minutes:
            latitude = fields[2]
            # north/south indicator (N or E)
            latitude_ns = fields[3]                
            # longitude, degress + minutes:
            longitude = fields[4]
            longitude_ew = fields[5]
            # fix status:
            #  0 = No Fix / Invalid
            #  1 = Standard GPS (2D/3D)
            #  2 = Differential GPS
            #  6 = Estimated (DR) Fix
            fix_status = fields[6]
            # satellite count used for fix:
            sat_count = fields[7]
            # field 8: HDOP, Horizontal Dilution of Precision ??
            # altitude: "MSL Altitude" (meters)
            altitude = fields[9]
            # field 10: fixed always M indicating meters
            # field 11: Geoid Separation ??
            # field 12 Units, Meters (fixed)
            # field 13: Age of differential corrections, Blank (Null) fields when DGPS is not used
            # field 14: Diff. Reference Station ID??
            # field 15: checksum in hex
            # field 16: CRLF
            if (fix_status == 1 or fix_status == 2):
                # 1=GPS SPS Mode, Fix valid, 2=Differential GPS, SPS Mode, Fix Valid
                ret = { 
                    'time': utc, 
                    'latitude': latitude, 
                    'latitude_ns': latitude_ns,
                    'longitude': longitude,
                    'longitude_ew': longitude_ew,
                    'satellites': sat_count 
                }
            elif fix_status == 0:
                # 0=Fix not available/invalid,
                pass
            else:
                print('GPS Fix message, but invalid fix status:', fix_status)
            pass
        elif msg == b'$GPTXT':
            # field 1: Total number of messages in this transmission, 01.. 99
            # field 2: Message number in this transmission, range 01..xx
            # field 3: Text identifier, u-blox GPS receivers specify the severity of the message with this number.
            # - 00 = ERROR
            # - 01 = WARNING
            # - 02 = NOTICE
            # - 07 = USER
            if len(fields) >= 4:
                level_num = fields[3].decode()
                level_map = { '00': 'ERROR', '01': 'WARNING', '02': 'NOTICE', '07': 'USER' }
                level = level_map[level_num] if level_num in level_map else '??'
            else:
                level = '?'
            if len(fields) > 4 and fields[4] is not None:
                # note that using .decode() here cowould throw  UnicodeError - so I guess there are some weird bytes in there.
                try:
                    text = fields[4].decode()
                    # remove the cr/lf at the end:
                    text = text.strip()
                except UnicodeError:
                    text = str(fields[4])
            else:
                text = ''
            print(f'GPS TXT {level}: {text}')
        elif msg == b'$GPGSA':
            # GNSS DOP and Active Satellites: The GPS receiver operating mode, satellites used for navigation, and DOP values.
            # 
            smode = fields[1]
            fix_status = fields[2]
            # the next 12 bytes are each the number of a satellite:
            satellites = []
            for i in range(3, 3+12):
                satellites.append(fields[i])
            if len(fields) >= 17:
                dilution_pos = fields[15]
                dilution_pos_h = fields[16]
                dilution_pos_v = fields[17]
            print(f"active satellites: {satellites}")
            pass
        elif msg == b'$GPRMC':
            # Recommended Minimum data
            utc = parse_time(fields[1])
            # is either A=position fixed, or V=no position fix.
            position_fix_status = fields[2]
            latitude = fields[3]
            latitude_ns = fields[4]
            longitude = fields[5]
            longitude_ew = fields[6]
            speed_over_ground_knots = fields[7]
            course_over_ground = fields[9]
            date = parse_date(fields[10])
            return {
                'time': utc,
                'position_fix_status': position_fix_status,
                'latitude': latitude,
                'latitude_ns':latitude_ns,
                'longitude': longitude,
                'longitude_ew': longitude_ew,
                'speed_over_ground_knots': speed_over_ground_knots,
                'course_over_ground': course_over_ground,
                'date': date
            }
        elif msg == b'$GPVTG':
            # TODO: Do we need this data?
            pass
        elif msg == b'$GPGSV':
            # TODO: Do we need this data?
            pass
        elif msg == b'$GPGLL':
            # TODO: Do we need this data?
            pass
        else:
            print('Unhandled GPS NMEA Message:', msg, fields)

                
                
        if (time.time() > max_timeout):
            return None
        utime.sleep_ms(500)
    
def from_hex(byt: int) -> int:
    '''
    returns the decimal value of the specified byte interpreted from a hexedecimal digit (for checksum in NMEA)
    '''
    if byt >= ord('A') and byt <= ord('F'):
        return byt - ord('A') + 10
    elif ord('a') <= byt <= ord('f'):
        return byt - ord('a') + 10
    else:
        return byt - ord('0')


while True:
    
    fix = get_fix(gpsModule)

    if fix:
        print("Received GPS fix:")
        print(fix)
    else:        
        print("No GPS fix.")
