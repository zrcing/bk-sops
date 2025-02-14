/**
* Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
* Edition) available.
* Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
* Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://opensource.org/licenses/MIT
* Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
* an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
* specific language governing permissions and limitations under the License.
*/
<template>
    <div class="atomdev-page">
        <div class="atom-edit-wrapper">
            <div class="tag-panel-col">
                <tag-panel :tags="tags" :disabled="isPreviewMode"></tag-panel>
            </div>
            <div class="form-panel-col">
                <template v-if="!atomStringError">
                    <form-panel
                        v-if="!hideFormPanel && !isPreviewMode"
                        :forms="forms"
                        @updateForm="updateForm"
                        @editForm="editForm"
                        @formSorted="formSorted">
                    </form-panel>
                </template>
                <div v-else class="error-message">{{ atomStringError }}</div>
            </div>
            <div class="config-panel-col">
                <div class="operate-area">
                    <bk-button theme="primary" :disabled="!!atomStringError" @click="onDownloadClick">{{ $t('下载') }}</bk-button>
                    <bk-button theme="default" :disabled="!!atomStringError" @click="onOpenPreviewMode">{{ $t('预览') }}</bk-button>
                    <bk-button theme="default" :disabled="isPreviewMode" @click="showUploadDialog = true">{{ $t('导入') }}</bk-button>
                </div>
                <config-panel
                    ref="configPanel"
                    :atom-config-str="atomConfigStr"
                    :api-code-str="apiCodeStr"
                    :atom-name="atomName"
                    :preview-mode="isPreviewMode"
                    @onNameChange="atomName = $event"
                    @atomEditError="atomEditError"
                    @atomConfigUpdate="atomConfigUpdate"
                    @apiCodeUpdate="apiCodeUpdate">
                </config-panel>
            </div>
        </div>
        <bk-sideslider
            :is-show="showAtomSetting"
            :quick-close="false"
            :width="600"
            :title="$t('插件配置')"
            :before-close="closeSettingPanel">
            <atom-setting
                slot="content"
                ref="atomSetting"
                v-if="showAtomSetting"
                :editing-form="editingForm"
                :atom-forms="atomForms">
            </atom-setting>
            <div slot="footer" class="slider-footer">
                <bk-button theme="primary" @click="onSaveAtomSetting">{{ $t('确认') }}</bk-button>
                <bk-button theme="default" @click="closeSettingPanel">{{ $t('取消') }}</bk-button>
            </div>
        </bk-sideslider>
        <bk-dialog
            v-model="showUploadDialog"
            :width="400"
            :mask-close="false"
            :title="$t('导入文件')"
            :loading="fileUploading">
            <div class="import-wrapper">
                <upload-read-file class="import-code" @uploaded="handleFormFile($event, 'formCode')">
                    <bk-button class="primary">{{ $t('前端代码') }}</bk-button>
                </upload-read-file>
                <upload-read-file class="import-code" @uploaded="handleFormFile($event, 'apiCode')">
                    <bk-button class="primary">{{ $t('后台代码') }}</bk-button>
                </upload-read-file>
            </div>
        </bk-dialog>
        <bk-dialog
            v-model="previewDialogShow"
            header-position="left"
            :fullscreen="true"
            :title="$t('预览')"
            :show-footer="false"
            :on-close="onPreviewClose">
            <div v-if="isPreviewMode" class="preview-panel">
                <render-form
                    class="render-form"
                    :scheme="atomConfig"
                    :form-option="renderFormOption"
                    v-model="renderFormData">
                </render-form>
            </div>
        </bk-dialog>
        <bk-dialog
            width="400"
            ext-cls="common-dialog"
            :theme="'primary'"
            :mask-close="false"
            :header-position="'left'"
            :title="$t('离开页面')"
            :value="isLeaveDialogShow"
            @confirm="onLeaveConfirm"
            @cancel="onLeaveCancel">
            <div class="leave-tips">{{ $t('系统不会保存您所做的更改，确认离开？') }}</div>
        </bk-dialog>
    </div>
</template>
<script>
    import JSZip from 'jszip'
    import { saveAs } from 'file-saver'
    import TagPanel from './TagPanel.vue'
    import FormPanel from './formPanel/FormPanel.vue'
    import ConfigPanel from './configPanel/ConfigPanel.vue'
    import AtomSetting from './atomSetting/AtomSetting.vue'
    import UploadReadFile from './UploadReadFile.vue'
    import RenderForm from '@/components/common/RenderForm/RenderForm.vue'
    import importTag from './importTag.js'
    import tools from '@/utils/tools.js'
    import { COMMON_ATTRS } from '@/components/common/RenderForm/formMixins.js'
    import serializeObj from '@/utils/serializeObj.js'
    const { components: TAGS, attrs: ATTRS } = importTag()

    // 用户可配置的公共属性
    const commonEditableAttrs = {}
    Object.keys(COMMON_ATTRS).reduce((acc, cur) => {
        if (['name', 'hookable', 'validation', 'default', 'hidden'].includes(cur)) {
            commonEditableAttrs[cur] = COMMON_ATTRS[cur]
        }
        return commonEditableAttrs
    }, commonEditableAttrs)

    export default {
        name: 'AtomDev',
        components: {
            TagPanel,
            FormPanel,
            AtomSetting,
            UploadReadFile,
            ConfigPanel,
            RenderForm
        },
        data () {
            const tags = this.getTagConfigMap(TAGS)
            return {
                tags,
                forms: [],
                atomName: '',
                atomConfig: [],
                atomForms: [],
                atomConfigStr: '',
                atomStringError: '',
                allowLeave: false,
                leaveToPath: '',
                contentChange: '', // 配置项内容有变更，用来做离开页面的二次确认
                apiCodeStr: '',
                editingForm: {},
                isPreviewMode: false,
                showAtomSetting: false,
                hideFormPanel: false,
                showUploadDialog: false,
                previewDialogShow: false,
                isLeaveDialogShow: false,
                fileUploading: false,
                renderFormOption: {
                    showGroup: false,
                    showHook: true,
                    showLabel: true,
                    showVarList: false
                },
                renderFormData: {}
            }
        },
        watch: {
            forms: {
                handler: function (val) {
                    this.getTransAtomConfig(val)
                    this.atomConfigStr = serializeObj(this.atomConfig)
                    this.atomForms = this.getAtomForms(val)
                },
                deep: true
            }
        },
        methods: {
            getTagConfigMap (tags) {
                const tagConfigMap = {}
                Object.keys(tags).forEach(tag => {
                    const tagAttrs = { ...commonEditableAttrs, ...ATTRS[tag] }
                    const type = tag.slice(3).replace(/[A-Z]/g, match => {
                        return `_${match.toLowerCase()}`
                    }).slice(1)
                    const attrs = {} // 对应标准插件配置项中的 attrs 属性
                    Object.keys(tagAttrs).reduce((acc, cur) => {
                        const item = tools.deepClone(tagAttrs[cur])
                        if (!item.inner) { // 不处理内部属性
                            if (item.hasOwnProperty('default')) {
                                if (item.type === Function) {
                                    item.value = item.default
                                } else {
                                    item.value = typeof item.default === 'function' ? item.default() : item.default
                                }
                            } else {
                                item.value = ''
                            }

                            delete item.default
                            attrs[cur] = item
                        }
                        return attrs
                    }, attrs)
                    tagConfigMap[tag] = {
                        tag,
                        config: {
                            type,
                            attrs,
                            events: [],
                            methods: {}
                        }
                    }
                    tagConfigMap['combine'] = {
                        tag: 'combine',
                        config: {
                            type: 'combine',
                            attrs: {
                                name: {
                                    type: String,
                                    required: true,
                                    value: ''
                                },
                                hookable: {
                                    type: Boolean,
                                    value: false
                                },
                                children: {
                                    value: []
                                }
                            },
                            events: [],
                            methods: {}
                        }
                    }
                })
                return tagConfigMap
            },
            transAtomConfig (forms) {
                const atomConfig = forms.map(item => {
                    const config = tools.deepClone(item.config)
                    if (config.type === 'combine' && Array.isArray(config.attrs.children.value)) {
                        config.attrs.children = this.transAtomConfig(config.attrs.children.value)
                    }
                    for (const key in config.attrs) {
                        if (key === 'children') {
                            continue
                        }
                        if (typeof config.attrs[key].value === 'function') {
                            config.attrs[key] = config.attrs[key].value
                        } else {
                            config.attrs[key] = tools.deepClone(config.attrs[key].value)
                        }
                    }
                    return config
                })
                return atomConfig
            },
            getTransAtomConfig (forms) {
                this.atomConfig = this.transAtomConfig(forms || this.forms)
            },
            updateForm (formList) {
                this.forms = formList
            },
            editForm (form) {
                this.showAtomSetting = true
                this.editingForm = form
            },
            formSorted (formList) {
                this.forms = formList
            },
            refreshFormPanel () {
                this.hideFormPanel = true
                setTimeout(() => {
                    this.hideFormPanel = false
                }, 0)
            },
            atomEditError (error) {
                this.atomStringError = error
            },
            // 代码片段转forms
            atomConfigToForms (formConfig) {
                return formConfig.map((item, index) => {
                    let tag = ''
                    if (item.type === 'combine') {
                        tag = 'combine'
                    } else {
                        const tagName = item.type.split('_').map(tp => tp.replace(/^\S/, s => s.toUpperCase())).join('')
                        tag = `Tag${tagName}`
                    }
                    const config = tools.deepClone(this.tags[tag].config)
                    config.tag_code = item.tag_code

                    if (item.hasOwnProperty('events')) {
                        config.events = item.events
                    }
                    if (item.hasOwnProperty('methods')) {
                        config.methods = item.methods
                    }
                    Object.keys(config.attrs).forEach(key => {
                        if (item.attrs.hasOwnProperty(key)) {
                            const attr = config.attrs[key]
                            attr.value = item.attrs[key]
                        }
                    })
                    if (item.type === 'combine') {
                        config.attrs.children.value = tools.deepClone(this.atomConfigToForms(config.attrs.children.value))
                    }
                    return {
                        config,
                        tag
                    }
                })
            },
            atomConfigUpdate (val) {
                this.contentChange = true
                const formConfig = tools.deepClone(val)
                const forms = this.atomConfigToForms(formConfig)
                const isFormChanged = !tools.isDataEqual(this.forms, forms)
                this.forms = forms
                if (isFormChanged) {
                    this.refreshFormPanel()
                }
            },
            apiCodeUpdate (val) {
                this.apiCodeStr = val
            },
            async onDownloadClick () {
                if (this.atomStringError) {
                    return
                }
                try {
                    await this.$refs.configPanel.validate()
                    const zip = new JSZip()
                    const formConfigContent = `(function(){\n$.${this.atomName}=${this.atomConfigStr}})()`
                    zip.file(`${this.atomName}.js`, formConfigContent)
                    zip.file(`${this.atomName}.py`, this.apiCodeStr)
                    zip.generateAsync({ type: 'blob' }).then(content => {
                        saveAs(content, 'bk_pulgin_code.zip')
                    })
                } catch (error) {
                    console.log(error)
                }
            },
            onOpenPreviewMode () {
                this.isPreviewMode = true
                this.previewDialogShow = true
                this.renderFormData = {}
            },
            onPreviewClose () {
                this.isPreviewMode = false
                this.previewDialogShow = false
            },
            handleFormFile (e, type) {
                const self = this
                this.fileUploading = true
                const files = e.target.files
                const fileReader = new FileReader()

                fileReader.readAsText(files[0], 'utf-8')
                fileReader.onload = function () {
                    self.fileUploading = false
                    self.showUploadDialog = false
                    self.isPreviewMode = false
                    if (type === 'formCode') {
                        self.atomConfigStr = fileReader.result
                        self.$refs.configPanel.atomConfigUpdate(fileReader.result)
                    } else {
                        self.apiCodeUpdate(fileReader.result)
                    }
                    self.$refs.configPanel.scroll(type)
                }
            },
            saveForm (forms, setItem) {
                for (let i = 0; i < forms.length; i++) {
                    const item = forms[i]
                    if (item.config.attrs.children) {
                        this.saveForm(item.config.attrs.children.value, setItem)
                    }
                    if (item.config.tag_code === this.editingForm.config.tag_code) {
                        forms[i] = setItem
                        return
                    }
                }
            },
            async onSaveAtomSetting () {
                const form = await this.$refs.atomSetting.validate()
                if (form) {
                    this.closeSettingPanel()
                    this.saveForm(this.forms, form)
                    // 手动触发更新代码展示面板数据
                    this.getTransAtomConfig(this.forms)
                    this.atomConfigStr = serializeObj(this.atomConfig)
                    this.refreshFormPanel()
                }
            },
            closeSettingPanel () {
                this.showAtomSetting = false
            },
            onLeaveConfirm () {
                this.allowLeave = true
                this.$router.push({ path: this.leaveToPath })
            },
            onLeaveCancel () {
                this.allowLeave = false
                this.leaveToPath = ''
                this.isLeaveDialogShow = false
            },
            // 获取扁平化数据 forms
            getAtomForms (forms) {
                let atomFroms = []
                for (let i = 0; i < forms.length; i++) {
                    const item = forms[i]
                    if (item.type === 'combine' && Array.isArray(item.attrs.children.value)) {
                        const localAtomForm = this.getAtomForms(item.config.attrs.children.value)
                        atomFroms = [...atomFroms, ...localAtomForm]
                    }
                    atomFroms.push({
                        tagCode: item.config.tag_code,
                        name: item.config.attrs.name.value
                    })
                }
                return atomFroms
            }
        },
        beforeRouteLeave (to, from, next) {
            if (this.allowLeave || !this.contentChange) {
                next()
            } else {
                this.leaveToPath = to.fullPath
                this.isLeaveDialogShow = true
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import '@/scss/mixins/scrollbar.scss';
    .atomdev-page {
        height: 100%;
    }
    .atom-edit-wrapper {
        display: flex;
        justify-content: space-around;
        height: 100%;
    }
    .tag-panel-col {
        width: 111px;
        height: 100%;
        border-right: 1px solid #dde4eb;
    }
    .form-panel-col {
        width: 750px;
        height: 100%;
    }
    .config-panel-col {
        width: calc(100% - 861px);
        height: 100%;
        background: #ffffff;
        border-left: 1px solid #dde4eb;
        .operate-area {
            padding: 10px 20px 9px;
            text-align: right;
            border-bottom: 1px solid #dde4eb;
        }
    }
    .slider-footer {
        padding: 0 20px;
    }
    .preview-panel {
        margin: 0 auto;
        width: 650px;
        height: 100%;
        background: #ffffff;
        overflow-y: auto;
        @include scrollbar;
        .render-form {
            padding: 30px 80px 20px 20px;
        }
    }
    .error-message {
        padding: 10px;
        color: #ff5656;
        word-break: break-all;
    }
    .import-wrapper {
        text-align: center;
        .import-code {
            display: inline-block;
            margin: 0 4px;
            width: 88px;
            height: 32px;
            border: none;
        }
    }
    .leave-tips {
        padding: 30px;
    }
</style>
