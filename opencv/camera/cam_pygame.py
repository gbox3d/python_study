#%%

import cv2 as cv

import os
from struct import *
import pygame
import time
import numpy as np
import multiprocessing
from multiprocessing import Queue

import time


from dotenv import load_dotenv


#%%

def rendering_task(queue):
    # pygame 초기화
    pygame.init()
    
    cap = cv.VideoCapture(0)

    if cap.isOpened():
        print(f'cam ok')
    else :
        print('connect failed')
        return
        
    screen_width = 640
    screen_height = 480
        
    # cap 의 해상도 설정
    cap.set(cv.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, screen_height)
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Set up text display
    font = pygame.font.Font(None, 36)  # Select the font and size

    fps = 999
    last_time = time.time()
    
    bStopRenderTask = False
    while bStopRenderTask == False:
        
        #fps 계산
        now = time.time()
        if now - last_time > 0:
            fps = 1 / (now - last_time)
        else:
            fps = 999
        last_time = now
        
        # openCV frame을 pygame surface로 변환
        
        ret,frame = cap.read()
        
        if not ret:
            print('Failed to capture frame')
            break
        
        frame_surface = pygame.surfarray.make_surface(cv.flip(np.rot90(cv.cvtColor(frame, cv.COLOR_BGR2RGB)),0))        
        # Clear the screen by camera frame
        screen.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))
        
        # Display FPS
        fps_info = f'FPS: {fps:.2f}'
        text_surface = font.render(fps_info, True, (255, 255, 255))  # White color
        screen.blit(text_surface, (10, 10))
        
        
        pygame.display.update()

        # Pygame 이벤트 처리 (종료 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bStopRenderTask = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bStopRenderTask = True
                elif event.key == pygame.K_q:
                    queue.put('quit')
            
    print('rendering_task end')
    queue.put('quit')  # 종료 신호 보내기
    
    pygame.quit()
    cap.release()
    
    
def console_task(queue):
    print('console_task start')
    #input text quit to exit
    while True:
        print('tick')
        
        if not queue.empty():
            command = queue.get()
            if command == 'quit':
                break
            
        time.sleep(1)
        
        
    print('console_task end')
    
# rendering_task()

if __name__ == '__main__':
    
    queue = Queue()
    
    rendering_process = multiprocessing.Process(target=rendering_task, args=(queue,))
    console_process = multiprocessing.Process(target=console_task,args=(queue,))

    rendering_process.start()
    console_process.start()
    
    # Check if the rendering process is still alive
    # while rendering_process.is_alive():
    #     time.sleep(0.5)  # Poll every 0.5 seconds
    #     console_process.terminate()

    rendering_process.join()
    console_process.join()
