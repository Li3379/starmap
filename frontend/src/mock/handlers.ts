/**
 * MSW (Mock Service Worker) 入口 —— 规范4（§17.5）Mock 优先。
 *
 * 流C 从 W3 起用 mock 独立开发，不依赖流B 真实接口。
 * W6 联调时，把 main.ts 里的 enableMocking() 调用去掉即可切换到真实接口。
 *
 * TODO(W3)：在此注册各接口的 mock handler，样例数据从 starmap-contracts/schemas/ 派生
 */
import { http, HttpResponse } from 'msw'

export const handlers = [
  // 示例：mock 全景图谱
  http.get('/api/v1/graph/panorama', () =>
    HttpResponse.json({
      nodes: [
        { id: 'pos-1', label: '算法工程师', type: 'position' },
        { id: 'skill-1', label: 'Python', type: 'skill' },
      ],
      edges: [{ source: 'pos-1', target: 'skill-1' }],
    }),
  ),
]
