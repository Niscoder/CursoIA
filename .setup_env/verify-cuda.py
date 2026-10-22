import sys
import platform
import subprocess
import torch

# Script que testa cuda

def section(title):
    print(f"\n{'=' * 55}")
    print(title)
    print('=' * 55)


def main():
    section("1. Ambiente Python")

    print("Python:", sys.version)
    print("Sistema:", platform.platform())
    print("Executável:", sys.executable)
    print("PyTorch:", torch.__version__)
    print("PyTorch instalado em:", torch.__file__)
    print("Runtime CUDA:", torch.version.cuda)

    section("2. Driver NVIDIA")

    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        print(result.stdout)
    except FileNotFoundError:
        print("ERRO: nvidia-smi não encontrado.")
        print("Verifique a instalação do driver NVIDIA e o PATH.")
    except subprocess.CalledProcessError as exc:
        print("ERRO ao consultar o driver:")
        print(exc.stderr or exc.stdout)
    except subprocess.TimeoutExpired:
        print("ERRO: nvidia-smi excedeu o tempo limite.")

    section("3. Disponibilidade CUDA")

    print("CUDA disponível:", torch.cuda.is_available())

    if not torch.cuda.is_available():
        print("\nFALHA: PyTorch não consegue acessar a GPU.")
        print("Verifique:")
        print("- Se o driver NVIDIA está instalado e funcionando.")
        print("- Se a versão do driver é compatível com o runtime CUDA.")
        print("- Se o PyTorch instalado possui suporte a CUDA.")
        return 1

    print("Número de GPUs:", torch.cuda.device_count())

    for index in range(torch.cuda.device_count()):
        print(f"GPU {index}:", torch.cuda.get_device_name(index))
        properties = torch.cuda.get_device_properties(index)
        print("Memória total:", f"{properties.total_memory / 1024**3:.2f} GiB")
        print("Compute capability:", f"{properties.major}.{properties.minor}")

    section("4. Teste real de processamento")

    try:
        device = torch.device("cuda:0")

        a = torch.randn(2048, 2048, device=device)
        b = torch.randn(2048, 2048, device=device)
        c = a @ b

        torch.cuda.synchronize()

        print("Dispositivo:", c.device)
        print("Formato do resultado:", tuple(c.shape))
        print("Resultado finito:", torch.isfinite(c).all().item())
        print("Uso de memória alocada:",
              f"{torch.cuda.memory_allocated(0) / 1024**2:.2f} MiB")

        assert c.device.type == "cuda"
        assert torch.isfinite(c).all().item()

    except Exception as exc:
        print("FALHA durante o teste CUDA:", repr(exc))
        return 1

    section("5. Resultado")

    print("SUCESSO: PyTorch executou operações na GPU NVIDIA.")
    print("O ambiente CUDA está funcional neste momento.")

    return 0


if __name__ == "__main__":
    sys.exit(main())