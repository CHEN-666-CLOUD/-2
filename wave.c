#include "wave.h"
#include <math.h>
#include <stdio.h>
#include "usart.h"
#include "Delay.h"

// ------- 需要和main.c保持一致参数定义 --------
#define N   70
#define AMP 4095

extern float wave[N];

// 生成一周期的汉宁窗调制正弦波
void Generate_Hann_Sine_Wave(float freq, float fs) {
    for(int n = 0; n < N; n++) {
        float hann = 0.5f * (1.0f - cosf(2.0f * 3.1415926f * n / (N-1)));
        float sine = sinf(2.0f * 3.1415926f * freq * n / fs);
        wave[n] = (AMP/2.0f) * (hann * sine + 1.0f); // 单边输出，范围0~AMP
    }
}