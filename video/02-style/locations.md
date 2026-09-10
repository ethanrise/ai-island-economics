# 场景视觉设定

本文件用于先生成并锁定主要地点。后续镜头优先复用这些地点的标准参考图。

## 1. 小岛全景

功能：开场、时间推进、结尾。

视觉设定：

- 中等大小温带/亚热带海岛；
- 有港口、小镇、农田、低层工业区、少量山坡和海岸；
- 总体生活化，不是度假天堂，也不是大都市；
- 建筑密度中低；
- 近未来基础设施自然融入，不突出炫技。

标准提示词：

> Wide aerial establishing view of a small inhabited island with about one thousand residents, compact coastal town, modest harbor, patchwork farmland, low-rise industrial district, winding roads, green hills and blue sea, believable near-future infrastructure subtly integrated into everyday life, calm morning atmosphere, warm coastal sunlight, cinematic editorial realism, muted blue and cream palette, human-scale settlement, no skyscrapers, no cyberpunk, no text, no logo

## 2. 岛上镇中心

功能：居民日常、商店、公共生活、后期富足生活场景。

标准提示词：

> Street-level view of a small island town center, low-rise mixed-use buildings, grocery shop, bakery, clinic and community spaces, pedestrians and bicycles, restrained near-future delivery automation subtly present, clean but lived-in environment, warm coastal daylight, cinematic editorial realism, muted blue-gray and warm cream palette, no neon, no megacity, no text artifacts

## 3. 林森农场

功能：最早的人机协作、生产率提升。

标准提示词：

> Medium-wide view of Lin Sen's practical island farm, vegetable fields and modest greenhouse structures, storage shed, small utility vehicle, irrigation equipment, believable working landscape near the coast, room for a compact intelligent work robot to operate, warm early morning light, cinematic editorial realism, grounded near-future agriculture, natural colors, no futuristic mega-farm, no text

建议生成三个状态：

- A：传统人工为主；
- B：林森 + 小工协作；
- C：高度自动化但仍保持同一场地结构。

## 4. 周启仓库

功能：劳动变化最重要的连续场景。

标准提示词：

> Interior of a medium-sized island logistics warehouse, recognizable fixed architecture, tall but not enormous shelving, loading area, pallets and packaged everyday goods, practical industrial lighting, clear central aisle, believable present-day foundation with room for gradual automation, cinematic editorial realism, restrained blue-gray palette, no sci-fi spaceship design, no text

必须生成三阶段：

- A：多人手工搬运；
- B：人和自动搬运设备共存；
- C：几乎无人，机器人持续运行。

三张图构图和建筑结构尽量一致。

## 5. 港口

功能：捕鱼、人工搬货、无人运输。

标准提示词：

> Working harbor of a small inhabited island, fishing boats, modest cargo pier, low warehouse buildings, forklifts and small trucks, practical coastal infrastructure, blue sea and distant hills, believable near-future automation introduced gradually, cinematic editorial realism, natural daylight, no giant container megapoort, no text

## 6. 自动化工厂

功能：黑灯工厂、生产过剩、减产。

标准提示词：

> Interior of a clean medium-scale automated factory on a small island, modular production cells, industrial robotic arms, conveyors and inspection systems producing ordinary consumer goods, practical architecture, believable high automation rather than science fiction, cool-neutral industrial light with warm highlights, cinematic editorial realism, no humanoid army, no hologram overload, no text

需要三个状态：高速生产 / 夜间少人运行 / 生产线逐渐停下。

## 7. 陈曦的 AI 控制中心

功能：表现 AI、算力、物流和设备协同。

标准提示词：

> Modest but advanced operations room for an island AI and automation company, wall displays showing abstract logistics flows, energy use and machine status, several normal workstations, clean restrained architecture, Chen Xi observing the system, believable near-future technology, dark blue-gray accents, soft indirect light, cinematic editorial realism, no giant holographic globe, no unreadable interface text

## 8. 公共会议空间

功能：苏岚组织制度讨论。

标准提示词：

> Small community assembly room on a coastal island, circular or semi-circular seating, ordinary residents gathered for a thoughtful public discussion, Su Lan facilitating calmly, simple wood and light-colored materials, large windows with soft daylight, non-governmental community atmosphere, cinematic editorial realism, no flags, no party symbols, no formal parliament imagery, no text

## 9. 韩木面包店

功能：从“效率”转向“关系、手艺、真实”。

标准提示词：

> Intimate neighborhood bakery in a small island town at early morning, warm wood, simple bread shelves, open workbench, visible hand-made bread, soft golden window light, a few familiar local customers, lived-in and personal rather than luxury commercial, cinematic editorial realism, warm restrained palette, no chain-store branding, no text

## 10. 广场棋桌

功能：陆远与朋友下棋。

标准提示词：

> Quiet public square in a small coastal island town, shade trees, stone or wooden chess tables, a few older residents spending time together, relaxed late-afternoon atmosphere, modest buildings in background, human-centered everyday life, cinematic editorial realism, warm natural light, no text

## 11. 周启的家

功能：账户、星期一清晨、生活改变。

标准提示词：

> Simple comfortable apartment of an ordinary island resident, modest contemporary furniture, large window with soft coastal daylight, practical and lived-in rather than luxurious, subtle signs of personal life, calm near-future atmosphere with unobtrusive digital devices, cinematic editorial realism, muted cream and blue-gray palette, no text

## 12. 海边步道 / 海岸

功能：稀缺土地、周启散步、结尾哲思。

标准提示词：

> Quiet coastal walking path on a small inhabited island, natural shoreline, modest homes in the distance, blue sea, grass and low shrubs, spacious horizon, soft golden-hour light, reflective human-centered mood, cinematic editorial realism, restrained colors, no resort glamour, no text

## 场景一致性原则

1. 同一地点在不同时间阶段，建筑结构不变化，只改变自动化密度、人物数量和光线。
2. 小岛所有地点的建筑语言应统一：低层、朴素、沿海、真实可居住。
3. 不生成摩天楼、超级城市、空中车流或宏大科幻设施。
4. 场景标准图确认后再进入 `03-keyframes/` 批量生成。
