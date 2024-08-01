import modulesConfig from './core_modules.json';
import customModulesConfig from './custom_modules.json';

interface ModuleConfig {
    enum: string;
    component: string;
    text: string;
}

const coreModules: ModuleConfig[] = modulesConfig.modules;
const customModules: ModuleConfig[] = customModulesConfig.modules;

const modules: ModuleConfig[] = [...coreModules, ...customModules];

export default modules;
