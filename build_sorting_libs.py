# A script to build external dependencies

import os
import subprocess
import platform


def basedir():
    return os.path.abspath(os.path.dirname(__file__))


def cub_include():
    return '-I%s/thirdparty/cub' % basedir()


def mgpu_include():
    return '-I%s/thirdparty/moderngpu/src' % basedir()


def lib_dir():
    return '%s/lib' % basedir()


def run_shell(cmd):
    print(cmd)
    subprocess.check_call(cmd, shell=True)


def library_extension():
    p = platform.system()
    if p == 'Linux':
        return 'so'
    if p == 'Windows':
        return 'dll'


def gencode_flags():
    # Generate code for all known architectures
    GENCODE_SMXX = "-gencode arch=compute_{CC},code=sm_{CC}"
    GENCODE_SM53 = GENCODE_SMXX.format(CC=53)
    GENCODE_SM60 = GENCODE_SMXX.format(CC=60)
    GENCODE_SM61 = GENCODE_SMXX.format(CC=61)
    GENCODE_SM62 = GENCODE_SMXX.format(CC=62)
    GENCODE_SM70 = GENCODE_SMXX.format(CC=70)
    GENCODE_SM72 = GENCODE_SMXX.format(CC=72)
    GENCODE_SM75 = GENCODE_SMXX.format(CC=75)
    GENCODE_SM80 = GENCODE_SMXX.format(CC=80)
    GENCODE_SM86 = GENCODE_SMXX.format(CC=86)

    # Provide forward-compatibility to architectures beyond CC 8.6
    GENCODE_COMPUTEXX = "-gencode arch=compute_{CC},code=compute_{CC}"
    GENCODE_COMPUTE86 = GENCODE_COMPUTEXX.format(CC=86)

    # Concatenate flags
    SM = []
    SM.append(GENCODE_SM53)
    SM.append(GENCODE_SM60)
    SM.append(GENCODE_SM61)
    SM.append(GENCODE_SM62)
    SM.append(GENCODE_SM70)
    SM.append(GENCODE_SM72)
    SM.append(GENCODE_SM75)
    SM.append(GENCODE_SM80)
    SM.append(GENCODE_SM86)
    SM.append(GENCODE_COMPUTE86)
    return ' '.join(SM)


def build_cuda(srcdir, out, ins, includes):
    # Allow specification of nvcc location in NVCC env var
    nvcc = os.environ.get('NVCC', 'nvcc')

    opt = '--extended-lambda --compiler-options "-fPIC"'

    ext = library_extension()
    output = os.path.join(lib_dir(), '%s.%s' % (out, ext))
    inputs = ' '.join([os.path.join(srcdir, p)
                       for p in ins])
    threads = f'-t{os.cpu_count()}'
    args = f'{threads} {opt} {includes} -O3 {gencode_flags()} --shared -o {output} {inputs}'
    cmd = ' '.join([nvcc, args])
    run_shell(cmd)


def build_radixsort():
    build_cuda(srcdir=lib_dir(),
               out='pyculib_radixsort',
               ins=['cubradixsort.cu'],
               includes=cub_include(), )


def build_mgpusort():
    build_cuda(srcdir=lib_dir(),
               out='pyculib_segsort',
               ins=['mgpusort.cu'],
               includes=mgpu_include(), )


if __name__ == '__main__':
    build_radixsort()
    build_mgpusort()
