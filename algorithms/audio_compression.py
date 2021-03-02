import torch
import torchaudio
import math

def fft(x):
    try:
        x.shape[2]
    except BaseException:
        x = x.reshape(1, x.shape[0], -1)

    m = x.shape[0]
    batch = x.shape[1]
    N = x.shape[2]

    if math.log2(N) % 1 > 0:
        while math.log2(x.shape[2]) % 1 > 0:
            A = torch.tensor([[0] * batch])
            x = (torch.cat((x[0].T, A)).T).reshape(1, batch, -1)

    N_min = min(N, 2)

    n = torch.arange(N_min)
    k = n[:, None]
    cos = torch.cos(2 * math.pi * n * k / N_min).view(N_min, -1)
    sin = torch.sin(-2 * math.pi * n * k / N_min).view(N_min, -1)
    X_real = cos @ x.view(m, batch, N_min, -1)
    X_im = sin @ x.view(m, batch, N_min, -1)

    while X_real.shape[2] < N:
        shape = X_real.shape[3] // 2
        arange = torch.arange(X_real.shape[2])
        X_r_even = X_real[:, :, :, : shape]
        X_r_odd = X_real[:, :, :, shape:]
        X_i_even = X_im[:, :, :, : shape]
        X_i_odd = X_im[:, :, :, shape:]
        f_r = torch.cos(-1 * math.pi * arange / X_real.shape[2]).view(-1, 1)
        f_i = torch.sin(-1 * math.pi * arange / X_im.shape[2]).view(-1, 1)
        P_r = f_r * X_r_odd - f_i * X_i_odd
        P_i = f_r * X_i_odd + f_i * X_r_odd
        X_real = torch.cat([X_r_even + P_r, X_r_even - P_r], dim=2)
        X_im = torch.cat([X_i_even + P_i, X_i_even - P_i], dim=2)

    return torch.cat([X_real[:, :, :N // 2 + 1, :], X_im[:, :, :N // 2 + 1, :]], axis=3)
  
  def stft(x, n_fft, hop_length, win_length):
    if win_length <= 0 or hop_length <=0:
        raise ValueError('parametres should be positive numbers')
    if win_length > x.shape[1]:
        raise ValueError('too big win_length')
    if hop_length > win_length:
        raise ValueError('hop should be smaller than window')
    
    start_points = torch.arange(0, x.shape[1], hop_length)
    stop_points = start_points + win_length
    
    index = [i <= x.shape[1] for i in stop_points.tolist()]
    start_points = start_points.reshape(1, start_points.shape[0])[0][index]
    stop_points = stop_points.reshape(1, stop_points.shape[0])[0][index]
    t = torch.Tensor(x.shape[0], win_length // 2 + 1, start_points.shape[0], 2)
    window = torch.hann_window(1024)
    for i in range(x.shape[0]):
        x_segments = [ x[i][start:stop,...] for start, stop in zip(start_points,
        stop_points)]
        x_segments = torch.stack(x_segments, axis=1)
        window = torch.hann_window(1024)
        res = x_segments.T * window
        t[i] = fft(res).transpose(1, 2)
    return t
  
  def MelSpectogram(x, sample_rate, n_fft, win_length, hop_length, n_mels = 80,
                  f_min = 0, f_max = 8000, power = 1.):
    spec = torch.stft(x, n_fft, hop_length, win_length, window=torch.hann_window(win_length))
    spec = spec.pow(2.).sum(-1).pow(0.5 * power)
    freqs = torch.linspace(0, sample_rate // 2, spec.shape[1])
    m_min = 1127.0 * math.log(1.0 + (f_min / 700.0))
    m_max = 1127.0 * math.log(1.0 + (f_max / 700.0))
    m_points = torch.linspace(m_min, m_max, n_mels + 2)
    f_points = 700.0 * (torch.exp(m_points / 1127.0) - 1.0)
    f_diff = f_points[1:] - f_points[:-1]
    slopes = f_points.unsqueeze(0) - freqs.unsqueeze(1) #
    down_slopes = (- 1.0 * slopes[:, :-2]) / f_diff[:-1]
    up_slopes = slopes[:, 2:] / f_diff[1:]
    fb = torch.max(torch.zeros(1), torch.min(down_slopes, up_slopes))
    mel_spectogram = (spec.transpose(1, 2) @ fb).transpose(1, 2)
    return mel_spectogram

