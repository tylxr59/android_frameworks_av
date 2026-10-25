#include <memory>
#include <vector>
#include <cassert>
namespace android { struct VideoCapabilities { struct PerformancePoint { int id; }; std::vector<PerformancePoint> points; VideoCapabilities(){for(int i=0;i<12;i++)points.push_back({i});} const auto& getSupportedPerformancePoints()const{return points;} }; }
CODE_UNDER_TEST
int main(){
 std::weak_ptr<android::VideoCapabilities> weak;
 std::unique_ptr<ACodecPerformancePoint> held;
 {auto caps=std::make_shared<android::VideoCapabilities>();weak=caps;
  {ACodecVideoCapabilities wrapper(caps);assert(wrapper.mPerformancePoints.size()==12);held=std::make_unique<ACodecPerformancePoint>(wrapper.mPerformancePoints[3]);}
  assert(!weak.expired());}
 assert(!weak.expired());assert(held->mPerformancePoint->id==3);held.reset();assert(weak.expired());
 for(int i=0;i<100;i++){auto caps=std::make_shared<android::VideoCapabilities>();ACodecVideoCapabilities wrapper(caps);auto copy=wrapper;assert(copy.mPerformancePoints[11].mPerformancePoint->id==11);}
}
