#include "stm32f10x.h"
#include "usart.h"
#include "wave.h"
#include "Delay.h"
#include <stdio.h>

// -------- 修改为70kHz波形相关参数 --------
#define WAVE_FREQ   70000     // 输出信号频率70kHz
#define SAMPLE_RATE 1000000   // 采样率1MHz
#define N           70        // 波形点数（比如输出1个周期：1MHz/70kHz=14，建议多几个周期如70点）
#define AMP         4095      // 振幅

float wave[N];

int main(void) {
    USART1_Init(115200);
    Generate_Hann_Sine_Wave(WAVE_FREQ, SAMPLE_RATE);

    int idx = 0;
    while(1) {
        // 每1/SAMPLE_RATE秒发送一个采样点
        printf("%d\n", (uint16_t)wave[idx]);
        idx++;
        if(idx >= N) idx = 0; // 循环
        Delay_us(1000000/SAMPLE_RATE); // 采样周期（单位us）
    }
}