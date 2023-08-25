#%%
import asyncio

async def loop_one():
    for i in range(5):
        print("Loop One, iteration:", i)
        await asyncio.sleep(1)
    print("Loop One is done!")

async def loop_two():
    for i in range(3):
        print("Loop Two, iteration:", i)
        await asyncio.sleep(2)
    print("Loop Two is done!")

async def loop_three():
    for i in range(2):
        print("Loop Three, iteration:", i)
        await asyncio.sleep(0)
    print("Loop Three is done!")

async def main():
    # 두 개의 루프를 동시에 실행
    await asyncio.gather(loop_one(), loop_two(),loop_three())
#%%
# 이벤트 루프 실행
asyncio.run(main())

print("All loops are done!")

# %%
