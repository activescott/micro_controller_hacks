#import info
#info.print_info()

from qmc5883l import Compass


c = Compass(13, 16)

print(f"compas says {c.read()}")