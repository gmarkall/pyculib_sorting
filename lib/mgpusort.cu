#include <stdint.h>
#include <moderngpu/context.hxx>
#include <moderngpu/kernel_segsort.hxx>
#include "dllexport.h"

namespace mgpu{
	std::string stringprintf(const char* format, ...) { return std::string(); }
}

namespace {

template<class Tkey, class Tval>
void segsortpairs(Tkey *d_keys,
  Tval *d_vals,
  int N,
  const int *d_segments,
  unsigned NumSegs,
  cudaStream_t stream)
{

  mgpu::standard_context_t context;
  mgpu::segmented_sort(d_keys, d_vals, N, d_segments, NumSegs, mgpu::less_t<Tkey>(), context);

}

} // end static namespace


extern "C" {

#define WRAP(F, Tkey, Tval)												\
DLLEXPORT void segsortpairs_##F( Tkey *d_keys,                          \
					   Tval *d_vals,									\
					   unsigned N,										\
					   const int *d_segments,							\
					   unsigned NumSegs,								\
					   cudaStream_t stream	)							\
{  segsortpairs(d_keys, d_vals, N, d_segments, NumSegs, stream);  }

WRAP(int32, int32_t, unsigned)
WRAP(int64, int64_t, unsigned)
WRAP(uint32, uint32_t, unsigned)
WRAP(uint64, uint64_t, unsigned)
WRAP(float32, float, unsigned)
WRAP(float64, double, unsigned)


}
