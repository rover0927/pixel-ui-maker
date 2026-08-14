# 黑客赛博朋克个人主页 — Cyber Geek Home Vue Demo

按 pixel-ui-maker 的「暗黑终端极客 × 黑客赛博朋克」风格实现的 Vue 3 + Vite 个人主页 demo:
近黑深空画布 + 霓虹青主强调 + 洋红辅强调,内置 JIEJOE 蒸馏动态效果
(`geek-btn-wipe` / `geek-float-rise` / `geek-marquee` / `geek-crt-ripple` / `geek-particle-bg`)。

## 运行

```bash
npm install
npm run dev     # 开发预览
npm run build   # 构建产物
```

## 结构

```
src/
  components/
    GeekNav.vue            # 固定顶栏导航（logo + 菜单 + CONTACT 擦除按钮）
    GeekHero.vue           # hero：glitch 标题 + 打字机 + CRT 屏 + 粒子网络 + 浮动像素画
    GeekMarquee.vue        # 四向滚动光带分割带（geek-marquee）
    GeekAbout.vue          # 关于（打字机）
    GeekSkills.vue         # 技能标签
    GeekProjects.vue       # 项目卡片
    GeekPhotos.vue         # 霓虹像素拍立得
    GeekContact.vue        # 联系（TRANSMIT 擦除按钮）
    GeekFooter.vue         # 页脚
    GeekParticleBg.vue     # 背景像素粒子网络（geek-particle-bg）
    GeekBtnWipe.vue        # 双层擦除按钮（geek-btn-wipe）
  composables/
    useParticleBg.js       # 粒子网络引擎（原生 Canvas，无依赖）
    useCrtRipple.js        # CRT 水波纹驱动（feTurbulence seed/scale）
    useTypewriter.js       # 终端打字机
  assets/geek-homepage.css # 主题样式（风格锁定）
  App.vue                  # 页面组装 + 共享 CRT 滤镜 defs
ui_spec.md                 # 设计规范（cyber-geek 主题）
```

## 命名约定

组件统一 `Geek*` PascalCase(对应 `geek-*` CSS 类),composables 统一 `use*` camelCase,
主题资产统一 `geek-homepage.css`。组件间不共享脚本库,每个 composable 独立无依赖。
