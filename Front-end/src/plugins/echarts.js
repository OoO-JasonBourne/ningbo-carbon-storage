// echarts.js
import * as echarts from 'echarts/core';
import { TooltipComponent, LegendComponent } from 'echarts/components';
import { PieChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { GraphicComponent } from 'echarts/components';

// 使用 echarts.use 安装需要的组件
echarts.use([
    TooltipComponent,
    LegendComponent,
    PieChart,
    CanvasRenderer,
    GraphicComponent
]);

export default echarts;
