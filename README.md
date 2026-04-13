![visitors](https://img.shields.io/badge/visitantes-0-blue) ![license](https://img.shields.io/badge/licença-CC%20BY--SA%204.0-lightgrey) ![language](https://img.shields.io/badge/idioma-português-brightgreen) ![tech](https://img.shields.io/badge/tecnologias-Python%203.8%2B%20%7C%20Jupyter%20Notebook%20%7C%20Machine%20Learning%20%7C%20STM32%20%7C%20FreeRTOS-orange) ![status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow) ![size](https://img.shields.io/badge/tamanho-médio-ff69b4) ![last-commit](https://img.shields.io/badge/último%20commit-n/d-gray)

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:1a56db,100:10b981&height=250&section=header&text=Projeto%20Magnetostricção&fontSize=60&fontColor=ffffff&animation=fadeIn" alt="Header Animado do Projeto Magnetostricção">
</p>

## Visão Geral

Este projeto implementa uma solução completa para **diagnóstico de saúde de transformadores de alta potência** através da análise de ruídos de magnetostricção com apoio de técnicas de Machine Learning. A solução abrange desde a geração de dados sintéticos até a implementação em hardware embarcado (STM32) para monitoramento em tempo real.

## Estrutura do Projeto

O projeto está organizado em múltiplos módulos que trabalham em conjunto:

### Módulos Principais

- **`simulador/`**: Sistema completo para simulação, análise e classificação de ruídos de magnetostricção
  - Gerador de amostras sintéticas realistas
  - Interface gráfica para análise em tempo real
  - Implementação de redes neurais (CNN, RNN, SVM, etc.)
  - Conversão para TinyML/STM32

- **`magnetostriccao_firmware/`**: Firmware para microcontroladores STM32 com FreeRTOS
  - Implementação embarcada do classificador
  - Interface com sensores e atuadores
  - Otimizado para processamento em tempo real

- **`magnetostriccao_firmware_freertos/`**: Variante do firmware com FreeRTOS completo
  - Sistema operacional em tempo real
  - Múltiplas tarefas concorrentes
  - Gerenciamento avançado de recursos

- **`magnetostriccao_firmware_sem_freertos/`**: Firmware bare-metal (sem RTOS)
  - Implementação direta em hardware
  - Baixo consumo de recursos
  - Ideal para aplicações simples

- **`DSTRM-STM32N6/`**: Projeto STM32CubeIDE para STM32N6
  - Configuração completa de periféricos
  - Drivers HAL
  - Sistema embarcado completo

- **`Apresentação/`**: Documentação de apresentação do projeto
  - Slides técnicos
  - Documentação de PICH
  - Material de divulgação

### Metodologia PDCL

Este projeto segue a metodologia **PDCL (Plan, Do, Check, Logs)**:

- **Plan**: Planejamento detalhado de funcionalidades e requisitos
- **Do**: Execução rigorosa do desenvolvimento documentado
- **Check**: Testes sistemáticos e validação de qualidade
- **Logs**: Registro completo de atividades e decisões

## Tecnologias Utilizadas

### Software
- **Python 3.8+**: Linguagem principal para desenvolvimento
- **TensorFlow/Keras**: Machine Learning e redes neurais
- **NumPy/SciPy**: Processamento numérico e de sinais
- **LibROSA**: Análise de áudio
- **PyQt5**: Interface gráfica
- **Jupyter Notebook**: Análise e documentação

### Hardware
- **STM32**: Microcontroladores ARM Cortex-M
- **FreeRTOS**: Sistema operacional em tempo real
- **Sensores de áudio**: Captura de ruídos de magnetostricção
- **NeoPixel/OLED**: Interfaces de visualização

### Técnicas de Machine Learning
- **CNN**: Redes neurais convolucionais para classificação espectral
- **MFCC**: Extração de características cepstrais em frequência Mel
- **FFT**: Análise espectral de sinais
- **TinyML**: Otimização para dispositivos embarcados

## Fluxo de Trabalho

### 1. Geração de Dados
```bash
# Gerar amostras sintéticas
python simulador/gerador_amostras_magnetostriccao.py --total 1000

# Gerar ruídos urbanos realistas
python simulador/gerar_ruidos_urbanos.py
```

### 2. Treinamento de Modelos
```bash
# Executar interface gráfica
python simulador/simulador.py ./samples_realistas

# Treinar modelo CNN
python simulador/treinar_modelo.py --arquitetura CNN
```

### 3. Conversão para Embedded
```bash
# Converter modelo para STM32
python simulador/h5_to_stm32_tinyml.py model_CNN.h5
```

### 4. Implementação Embarcada
```bash
# Compilar firmware STM32
cd magnetostriccao_firmware
mkdir build && cd build
cmake ..
make
```

## Características Técnicas

### Análise de Sinais
- **Frequência**: Foco em 60Hz e harmônicas até 1kHz
- **Classes**: Normal (0), Intermediário (1), Falha (2)
- **Pré-processamento**: Filtros Butterworth, normalização, MFCCs

### Redes Neurais
- **CNN**: 16-32 filtros convolucionais, 64 neurônios densos
- **Entrada**: MFCCs 40xframes (formato imagem 2D)
- **Saída**: Classificação softmax em 3 classes
- **Otimização**: Adam, learning rate adaptativo

### Desempenho
- **Tempo real**: Processamento < 100ms por amostra
- **Memória**: Modelo otimizado para < 50KB (TinyML)
- **Precisão**: > 95% em dados de teste controlados

## Instalação e Configuração

### Pré-requisitos
- Python 3.8+ (recomendado 3.10)
- Git
- STM32CubeIDE (para desenvolvimento embarcado)
- Toolchain ARM GCC

### Ambiente Python
```bash
# Clonar repositório
git clone <repository-url>
cd Magnetostriccao

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r simulador/requirements.txt
# Windows: pip install -r simulador/requirements-windows.txt
```

### Hardware STM32
```bash
# Configurar toolchain
sudo apt-get install gcc-arm-none-eabi

# Compilar firmware
cd magnetostriccao_firmware
mkdir build && cd build
cmake ..
make flash
```

## Documentação

### Documentação Técnica
- **`docs/`**: Artigos e papers de referência
- **`simulador/docs/`**: Documentação de algoritmos e técnicas
- **`Apresentação/`**: Slides e material de apresentação

### Guias de Implementação
- **STM32 Base**: `simulador/stm32_base/README_STM32_PROJECT.md`
- **FreeRTOS**: Guia de configuração e uso
- **TinyML**: Conversão e otimização de modelos

## Contribuição

Este projeto segue metodologia PDCL rigorosa. Contribuições devem:

1. **Plan**: Documentar planejamento completo
2. **Do**: Implementar seguindo padrões estabelecidos  
3. **Check**: Realizar testes abrangentes
4. **Logs**: Registrar todas as atividades

### Padrões de Código
- Python: PEP 8, type hints, docstrings
- C/C++: MISRA C, comentários detalhados
- Git: commits semânticos, mensagens descritivas

## Licença

Este projeto está licenciado sob **CC BY-SA 4.0** - Creative Commons Attribution-ShareAlike 4.0 International.

## Status do Projeto

- **Desenvolvimento**: Ativo
- **Versão**: 1.0.0-alpha
- **Compatibilidade**: Python 3.8+, STM32F4/F7/H7
- **Testes**: Unitários e integração
- **Documentação**: Completa

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,50:1a56db,100:0f172a&height=100&section=footer&text=Fim%20da%20Visão%20Geral&fontSize=30&fontColor=ffffff&animation=fadeIn" alt="Footer Animado">
</p>

---

## Resumo Final

**Data de Criação**: 13/04/2026  
**Autor**: Carlos Delfino  
**Versão**: 1.0.0-alpha  
**Última Atualização**: 13/04/2026  
**Atualizado por**: Sistema automático  

### Histórico de Alterações

| Versão | Data | Alterações | Autor |
|--------|------|------------|-------|
| 1.0.0-alpha | 13/04/2026 | Criação inicial do README.md principal com estrutura completa do projeto, seguindo diretrizes Windsurf | Sistema automático |
| | | | |

### Notas de Versão
- Versão inicial com documentação completa
- Estrutura modular implementada
- Metodologia PDCL aplicada
- Compatibilidade multiplataforma
