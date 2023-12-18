import Vue from "vue";
import {
    Button,
    Select,
    Option, // 注意这里引入了 el-option
    Icon,
    Checkbox,
    CheckboxGroup,
    CheckboxButton,
    Dropdown,
    DropdownMenu,
    DropdownItem,
    Message,
    Tabs,
    TabPane,
    Dialog,
    Table,
    TableColumn,
    Tag
} from 'element-ui';

// 注册 Element UI 组件
Vue.component('ElButton', Button);
Vue.component('ElSelect', Select);
Vue.component('ElOption', Option); // 注册 el-option
Vue.component('ElIcon', Icon); // 注册 el-option
Vue.component('ElCheckbox', Checkbox); // 注册 el-option
Vue.component('ElCheckboxGroup', CheckboxGroup);
Vue.component('ElCheckboxButton', CheckboxButton)
Vue.component('ElDropdown', Dropdown)
Vue.component('ElDropdownMenu', DropdownMenu)
Vue.component('ElDropdownItem', DropdownItem)
Vue.component('ElTabs', Tabs)
Vue.component('ElTabPane', TabPane)
Vue.component('ElDialog', Dialog)
Vue.component('ElTable', Table)
Vue.component('ElTableColumn', TableColumn)
Vue.component('ElTag', Tag)



// 按需引入 Element UI 样式
import 'element-ui/lib/theme-chalk/button.css';
import 'element-ui/lib/theme-chalk/select.css';
import 'element-ui/lib/theme-chalk/option.css'; // 引入 el-option 样式
import 'element-ui/lib/theme-chalk/icon.css'; // 引入 el-option 样式
import 'element-ui/lib/theme-chalk/checkbox.css'; // 引入 el-option 样式
import 'element-ui/lib/theme-chalk/dropdown.css'; 
import 'element-ui/lib/theme-chalk/dropdown-menu.css'; 
import 'element-ui/lib/theme-chalk/dropdown-item.css'; 
import 'element-ui/lib/theme-chalk/tabs.css'; 
import 'element-ui/lib/theme-chalk/tab-pane.css'; 
import 'element-ui/lib/theme-chalk/dialog.css'; 
import 'element-ui/lib/theme-chalk/table.css'; 
import 'element-ui/lib/theme-chalk/table-column.css'; 
import 'element-ui/lib/theme-chalk/tag.css'; 



// 注册 message
Vue.prototype.$message = Message; // 将 Message 组件挂载到 Vue 实例上