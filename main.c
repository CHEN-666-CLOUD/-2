#include "stm32f10x.h"
#include "usart.h"
#include "wave.h"
#include "Delay.h"
#include <stdio.h>

// -------- �޸�Ϊ70kHz������ز��� --------
#define WAVE_FREQ   70000     // ����ź�Ƶ��70kHz
#define SAMPLE_RATE 1000000   // ������1MHz
#define N           70        // ���ε������������1�����ڣ�1MHz/70kHz=14������༸��������70�㣩
#define AMP         4095      // ���

float wave[N];

int main(void) {
    USART1_Init(115200);
    Generate_Hann_Sine_Wave(WAVE_FREQ, SAMPLE_RATE);

    int idx = 0;
    while(1) {
        // ÿ1/SAMPLE_RATE�뷢��һ��������
        printf("%d\n", (uint16_t)wave[idx]);
        idx++;
        if(idx >= N) idx = 0; // ѭ��
        Delay_us(1000000/SAMPLE_RATE); // �������ڣ���λus��
    }
}