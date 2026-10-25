# NDK codec capability ownership regression

Run `python3 run-host.py --output-dir /path/outside/the/source/tree` on a Linux
host with GCC's AddressSanitizer and UndefinedBehaviorSanitizer available.

The harness extracts the actual performance-point/video capability wrappers
from NdkMediaCodecInfoPriv.h. A small VideoCapabilities fixture supplies an owned
vector of immutable points. Tests cover copied wrappers, 100 teardown cycles,
and a retained performance point surviving both the wrapper and original owner.
It must release the owner once the final retained point is released.

The original ownership implementation fails; results on the fixed implementation
must be followed by public NDK lookup/enumeration and ordinary client teardown
on a real Android device. This harness does not validate codec encoding/decoding.
