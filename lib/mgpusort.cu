#include "dllexport.h"
#include <moderngpu/context.hxx>
#include <moderngpu/kernel_segsort.hxx>
#include <stdint.h>

namespace {

template <class key_t, class val_t>
void segsortpairs(key_t *d_keys, val_t *d_vals, uint32_t n_vals,
                  const int32_t *d_segments, uint32_t n_segs,
                  cudaStream_t stream) {

  mgpu::standard_context_t context;
  mgpu::segmented_sort(d_keys, d_vals, n_vals, d_segments, n_segs,
                       mgpu::less_t<key_t>(), context);
}

} // namespace

extern "C" {

#define WRAP(F, Tkey, Tval)                                                    \
  DLLEXPORT void segsortpairs_##F(Tkey *d_keys, Tval *d_vals, unsigned N,      \
                                  const int *d_segments, unsigned NumSegs,     \
                                  cudaStream_t stream) {                       \
    segsortpairs(d_keys, d_vals, N, d_segments, NumSegs, stream);              \
  }

WRAP(int32, int32_t, unsigned)
WRAP(int64, int64_t, unsigned)
WRAP(uint32, uint32_t, unsigned)
WRAP(uint64, uint64_t, unsigned)
WRAP(float32, float, unsigned)
WRAP(float64, double, unsigned)
}
