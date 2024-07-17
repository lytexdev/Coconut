// * This file is used to import all the modules
import modulesConfig from './modules.json';

interface ModuleConfig {
    enum: string;
    component: string;
    text: string;
}

const modules: ModuleConfig[] = modulesConfig.modules;

export default modules;
