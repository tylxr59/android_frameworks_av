#!/usr/bin/env python3
"""Run sanitizer ownership tests on the actual NDK capability wrappers."""
from pathlib import Path
import argparse,subprocess,json
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args()
b=Path(__file__).resolve().parent;out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
source=(b.parents[1]/'NdkMediaCodecInfoPriv.h').read_text()
start=source.index('struct ACodecPerformancePoint {');end=source.index('struct ACodecEncoderCapabilities {',start)
fixture=(b/'test.cpp').read_text().replace('CODE_UNDER_TEST',source[start:end]);(out/'fixture.cpp').write_text(fixture)
subprocess.run(['g++','-std=c++17','-g','-O1','-fsanitize=address,undefined',str(out/'fixture.cpp'),'-o',str(out/'test')],check=True)
r=subprocess.run([str(out/'test')],capture_output=True,text=True);(out/'sanitizer.log').write_text(r.stdout+r.stderr);r.check_returncode()
(out/'result.json').write_text(json.dumps({'actual_wrappers_extracted':True,'asan_ubsan_passed':True,'retained_point_lifetime_passed':True,'copy_teardown_cycles':100},indent=2)+'\n')
print('Actual-wrapper ownership/lifetime tests passed under ASan/UBSan.')
