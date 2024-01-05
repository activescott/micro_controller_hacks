from machine import Pin, UART
import time

class Gps:
    def __init__(self):
        # TODO: take in arguments here for opening the device or allow them to pass in a device with readline method?
        pass

    def open(self):
        device = UART(1)
        # per the ublox manual for Serial Port Output: "9600 Baud, 8 bits, no parity bit, 1 stop bit"
        # FYI: 9600 worked in my testing, but u-blox and micropython esp32 says it supports 115200,but i tried taht and it didn't work (may require sending some message to gps to adjust)
        device.init(baudrate=9600, tx=4, rx=36, bits=8, parity=None, stop=1)
        self.device = device
        self.info('GPS device opened:', self.device)
        EPOCH = const(0)
        self._last_message_received_at = EPOCH
        self._last_fix_at = EPOCH
    
    def close(self):
        if self.device is not None:
            self.device.deinit()
            self.device = None
    
    def __enter__(self):
        self.open()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def log(self, msg: str, *args: Any) -> None:
        tt = time.localtime()[3:6]
        prefix = '{:02d}:{:02d}.{:02d} '.format(*tt)
        args_str = ' '.join(map(str, args))
        print(prefix + msg + ' ' + args_str + "\n")

    def debug(self, msg: str, *args: Any) -> None:
        self.log('DEBUG: ' + msg, *args)
        
    def info(self, msg: str, *args: Any) -> None:
        self.log('INFO: ' + msg, *args)
    
    def warn(self, msg: str, *args: Any) -> None:
        self.log('WARN: ' + msg, *args)
    
    def error(self, msg: str, exception=None, *args: Any) -> None:
        if exception is not None:
            output = io.StringIO()
            sys.print_exception(exception, output)
            msg = msg + ' ' + output.getvalue()
            output.close()
        self.log('ERROR: ' + msg, *args)

    def status(self) -> (str, str, float):
        '''
        Returns the status of the GPS device as a tuple of `(device_status, fix_status, seconds_since_message, seconds_since_fix)`.

        device_status be one of the following:
        - 'alive'
        - 'dead'

        fix_status be one of the following:
        - 'fix'
        - 'no fix'

        seconds_since_last_message is the number of seconds since the last valid message was received from the device.
        '''
        # attempt to get a fix with a short timeout (this will cause a message to be read and a fresh fix to be attempted)
        self.position(0.25)
        since_message = time.time() - self._last_message_received_at
        since_fix = time.time() - self._last_fix_at 
        alive = 'alive' if since_message < 5 else 'dead'
        fix = 'fix' if since_fix < 10 else 'no fix'
        return (alive, fix, since_message, since_fix)

    def position(self, timeout=5) -> dict:
        # try until max_timeout seconds to get a GPS Fixed Position
        max_timeout = time.time() + timeout
        
        while True:
            # note buff is of type bytes:
            fields = self.read()
            msg = fields[0] if len(fields) > 0 else b''
            if msg == b'':
                # we ignore these messages as they failed checksum or were invalid
                pass
            elif msg == b'$GPGGA':
                # GGA: Global positioning system fix data message:
                self.debug(f'GPS fix message received: {fields}')
                # Current Time UTC:
                utc = parse_time(fields[1])
                # Latitude, Degress + minutes:
                latitude = fields[2]
                # north/south indicator (N or E)
                try:
                    # note b'0'[0] == ord('0')
                    fix_status = int(fields[6])
                except ValueError:
                    self.warn('Invalid fix status:', fields[6])
                    fix_status = 0

                # rest of the code remains unchanged
                latitude_ns = fields[3]                
                longitude = fields[4]
                longitude_ew = fields[5]
                sat_count = fields[7]
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
                    self._last_fix_at = time.time()
                    ret = { 
                        'time': utc,
                        'fix_status': fix_status,
                        'latitude': latitude, 
                        'latitude_ns': latitude_ns,
                        'longitude': longitude,
                        'longitude_ew': longitude_ew,
                        'satellites': sat_count
                    }
                    return ret
                elif fix_status == 0:
                    # 0=Fix not available/invalid,
                    pass
                else:
                    self.warn('GPS Fix message, but invalid fix status:', fix_status)
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
                smode = fields[1]
                fix_status = fields[2]
                # the next 12 bytes are each the number of a satellite:
                satellites = []
                for i in range(3, 3+12):
                    if (fields[i] != b''):
                        satellites.append(fields[i])
                if len(fields) >= 17:
                    dilution_pos = fields[15]
                    dilution_pos_h = fields[16]
                    dilution_pos_v = fields[17]
                if len(satellites) > 0:
                    self.info(f"active satellites: {satellites}")
                pass
            elif msg == b'$GPRMC':
                # Recommended Minimum data
                utc = parse_time(fields[1])
                # position_fix_status: A=Data VALID, V=Data Invalid (Navigation Receiver Warning)
                position_fix_status = fields[2]
                if position_fix_status == b'A':
                    self._last_fix_at = time.time()
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
            time.sleep_ms(100)

    def read(self):
        '''
        Parses a line from the GPS device.
        If the line is a valid NMEA line it returns it as a set of fields in a list.
        If the line is invalid, an empty list is returned.
        '''
        # to be a valid message the message must meet the following criteria:
        #  - Begin with a $
        #  - End with a CRLF sequence
        #  - The two hexedecimal digits preceeding the CRLF is a checksum. Those two characters are preceeded by a *.
        #    The checksum is the XOR of all characters between the $ and the *
        bits = self.device.readline()
        if bits == None:
            #self.debug('GPS returned nothing.')
            return []
        length = len(bits)
        if length < len('$GP...*hh..'):
            self.debug(f'GPS returned line with too short of a length ({length}).Full line was: {bits}')
            return []
        if bits[0:1] != b'$':
            self.debug(f'GPS message did not begin with "$" (was "{bits[0]}"). Ignoring.')
            return []
        # note: the checksum is absolutely necessary for UART. Very frequent mangled messages come through without it.
        # ends in CRLF preceded by two characters representing a hex number: https://en.wikipedia.org/wiki/NMEA_0183
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
        self._last_message_received_at = time.time()
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

if __name__ == '__main__':
    gps = Gps()
    with gps:
        while True:
            status = gps.status()
            print("Received GPS status:", status)

            fix = gps.position()

            if fix:
                print("Received GPS position:")
                print(fix)
            else:        
                print("No GPS fix.")
