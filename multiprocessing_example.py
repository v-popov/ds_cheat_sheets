import os
import multiprocessing
from tqdm import tqdm # for tracking progress


def dummy_func(data: dict):
    ans = []
    names = data['name']
    values = data['value']

    for name, value in zip(names, values):
        dummy_var = 0
        for _ in range(20000000):
            dummy_var += 1
        ans.append(f'{name}_{dummy_var + value}')

    return ans


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)

    # Generating Data
    length = 100
    names = [f'name_{i}' for i in range(length)]
    values = [i for i in range(length)]

    # Splitting Data in Chunks (for distributing accross cores)
    chunks = []
    chunk_size = 2
    for i in range(0, length, chunk_size):
        names_chunk = names[i:i + chunk_size]
        values_chunk = values[i:i + chunk_size]
        data_chunks = {'name': names_chunk, 'value': values_chunk}
        chunks.append(data_chunks)
    print(f'Chunk #0: {chunks[0]}')

    # Multiprocessing
    num_cpus_total = os.cpu_count()
    num_cpus_to_use = max(num_cpus_total - 1, 1)
    print(f'{num_cpus_to_use}/{num_cpus_total} CPUs will be used')

    with multiprocessing.Pool(processes=num_cpus_to_use) as pool:
        ans = list(
                        tqdm(
                            pool.imap(dummy_func,
                                      chunks),
                            total=length//chunk_size
                        )
        )
        print(ans)


# CMD Output:
# Chunk #0: {'name': ['name_0', 'name_1'], 'value': [0, 1]}
# 15/16 CPUs will be used
# 100%|██████████| 50/50 [00:07<00:00,  6.27it/s]
# [['name_0_20000000', 'name_1_20000001'], ['name_2_20000002', 'name_3_20000003'], ... ]