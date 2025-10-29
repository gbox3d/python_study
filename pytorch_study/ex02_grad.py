#%%
import torch

# 미분 (gradient) 계산

#%%
# 1. 'x = 2' 라는 지점에서 변화량을 추적하겠다고 설정
#    숫자 뒤에 .0을 붙여 소수점(float)으로 만들어야 기울기 계산이 가능합니다.
x = torch.tensor(2.0, requires_grad=True)

# 2. 간단한 연산 수행
#    수식: z = 3 * x²
y = x ** 2
z = y * 3

# 3. 'z'를 'x'에 대해 미분하라는 명령
z.backward()

# 4. 결과 확인
print(f"최종 결과 z: {z}")
print(f"x=2일 때, z를 x로 미분한 값 (x.grad): {x.grad}")


#%%
# 
# 1) requires_grad=True 로 설정
x = torch.randn(10, requires_grad=True)

# 2) 기본 연산들
y = x + 2
z = y * y * 3
z = z.mean()

# 확인용 출력
print("x =", x)
print("y =", y)
print("z =", z)

#%%
z.backward()
print(x.grad) # dz/dx

#%%

# y was created as a result of an operation, so it has a grad_fn attribute.
# grad_fn: references a Function that has created the Tensor
print(x) # created by the user -> grad_fn is None
print(y)
print(x.grad_fn) # 사용자가 직접 만든 텐서는 함수가 설정되지않는다.
print(y.grad_fn)

#%% Do more operations on y
z = y * y * 3
print(z)
z = z.mean()
print(z)

# backpropagation(역전파) 로 gradients(경사)값을 구하기
# 계산응 마치면 backward 함수를 호출할수있고, 거기서 모든 경사값은 자동으로 계산된다.
# 텐서에 대한 그래디언트(경사)값은 .grad에 저장된다.
# It is the partial derivate of the function w.r.t. the tensor
print(x.grad)
z.backward()
print(x.grad) # dz/dx

# Generally speaking, torch.autograd is an engine for computing vector-Jacobian product
# It computes partial derivates while applying the chain rule

#%% ------------- 텐서가 백터값일때
# Model with non-scalar output:
# If a Tensor is non-scalar (more than 1 elements), we need to specify arguments for backward() 
# specify a gradient argument that is a tensor of matching shape.
# needed for vector-Jacobian product

x = torch.randn(3, requires_grad=True)

y = x * 2
for _ in range(10):
    y = y * 2
    print(y)


print(y.shape)

v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float32)
y.backward(v)
print(x.grad)

# %%-------------
# Stop a tensor from tracking history:
# For example during our training loop when we want to update our weights
# then this update operation should not be part of the gradient computation
# - x.requires_grad_(False)
# - x.detach()
# - wrap in 'with torch.no_grad():'

# .requires_grad_(...) changes an existing flag in-place.
a = torch.randn(2, 2)
print(a.requires_grad)
b = ((a * 3) / (a - 1))
print(b.grad_fn)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)

# .detach(): get a new Tensor with the same content but no gradient computation:
a = torch.randn(2, 2, requires_grad=True)
print(a.requires_grad)
b = a.detach()
print(b.requires_grad)

#%% wrap in 'with torch.no_grad():'
a = torch.randn(2, 2, requires_grad=True)
print(a.requires_grad)
with torch.no_grad():
    print((a ** 2).requires_grad)
print((a ** 2).requires_grad)

#%% -------------
# backward() accumulates the gradient for this tensor into .grad attribute.
# !!! We need to be careful during optimization !!!
# Use .zero_() to empty the gradients before a new optimization step!
weights = torch.ones(4, requires_grad=True)

for epoch in range(3):
    # just a dummy example
    model_output = (weights*3).sum()
    model_output.backward()
    print(weights.grad)

    # optimize model, i.e. adjust weights...
    with torch.no_grad():
        weights -= 0.1 * weights.grad

    # this is important! It affects the final weights & output
    weights.grad.zero_()
    # print(weights)

print(weights)
print(model_output)

# Optimizer has zero_grad() method
# optimizer = torch.optim.SGD([weights], lr=0.1)
# During training:
# optimizer.step()
# optimizer.zero_grad()
# %%
