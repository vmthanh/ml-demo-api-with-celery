import GPUtil


class GPUUtils:
    @classmethod
    def get_gpu_memory_frac_by_size(cls, gpu_id, megabytes):
        if megabytes <= 0:
            return 0.0
        gpu_list = GPUtil.getGPUs()
        if not gpu_list:
            return 0.0
        if gpu_id >= len(gpu_list):
            return 0.0
        gpu = gpu_list[gpu_id]
        gpu_memory_frac = megabytes * 1.0 / gpu.memoryTotal
        gpu_memory_frac = max(0.0, min(1.0, gpu_memory_frac))
        return gpu_memory_frac
