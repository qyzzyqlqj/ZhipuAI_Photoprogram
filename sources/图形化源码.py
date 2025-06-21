import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, 
                             QTextEdit, QCheckBox, QFrame)
from PyQt5.QtGui import QFont, QIcon, QDesktopServices, QColor, QPalette
from PyQt5.QtCore import QUrl, Qt, QSettings
from zhipuai import ZhipuAI

class ImageGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("ZhipuAI", "ImageGenerator")
        self.initUI()
        
    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('智谱AI绘图工具')
        self.setGeometry(300, 300, 650, 450)
        
        # 创建字体
        title_font = QFont('Arial', 16, QFont.Bold)
        label_font = QFont('Arial', 10)
        link_font = QFont('Arial', 9)
        link_font.setUnderline(True)
        
        # 创建UI元素
        self.title_label = QLabel('智谱AI绘图工具', self)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # 需求输入
        self.prompt_label = QLabel('绘图需求描述:')
        self.prompt_label.setFont(label_font)
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText('请输入详细的绘图描述...')
        self.prompt_input.setMaximumHeight(100)
        
        # API密钥输入
        self.api_key_label = QLabel('API密钥:')
        self.api_key_label.setFont(label_font)
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText('请输入您的API密钥...')
        self.api_key_input.setEchoMode(QLineEdit.Password)
        
        # 加载保存的API密钥
        saved_api_key = self.settings.value("api_key", "")
        if saved_api_key:
            self.api_key_input.setText(saved_api_key)
        
        # 保存API密钥复选框
        self.save_api_check = QCheckBox('保存API密钥')
        self.save_api_check.setFont(label_font)
        self.save_api_check.setChecked(self.settings.value("save_api", True, type=bool))
        
        # 模型选择
        self.model_label = QLabel('选择模型:')
        self.model_label.setFont(label_font)
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            'cogview-4-250304 (最新、付费)',
            'cogview-4 (付费)',
            'cogview-3-flash (免费)'
        ])
        
        # 修复模型选择框样式问题
        self.model_combo.setStyleSheet("""
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #4CAF50;
                color: black;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # 生成按钮
        self.generate_btn = QPushButton('生成图像')
        self.generate_btn.setFont(QFont('Arial', 12, QFont.Bold))
        self.generate_btn.setStyleSheet('background-color: #4CAF50; color: white;')
        self.generate_btn.clicked.connect(self.generate_image)
        
        # 结果区域
        self.result_label = QLabel('生成结果:')
        self.result_label.setFont(label_font)
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setPlaceholderText('图像URL将显示在这里...')
        self.result_output.setStyleSheet("color: #0066cc;")
        
        # 打开链接按钮
        self.open_link_btn = QPushButton('在浏览器中打开')
        self.open_link_btn.setEnabled(False)
        self.open_link_btn.clicked.connect(self.open_url)
        
        # API密钥获取链接
        self.api_link_label = QLabel(
            '<a href="https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys" style="color: #0066cc;">'
            '获取API密钥</a>'
        )
        self.api_link_label.setFont(link_font)
        self.api_link_label.setOpenExternalLinks(True)
        self.api_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.api_link_label.setAlignment(Qt.AlignRight)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #cccccc;")
        
        # 布局管理
        main_layout = QVBoxLayout()
        
        # 标题布局
        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(15)
        
        # 输入区域布局
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.prompt_input)
        
        # API密钥行布局
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(self.api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        api_key_layout.addWidget(self.save_api_check)
        api_key_layout.addWidget(self.api_link_label)
        
        input_layout.addLayout(api_key_layout)
        
        # 模型选择布局
        model_layout = QHBoxLayout()
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        input_layout.addLayout(model_layout)
        input_layout.addSpacing(15)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.generate_btn)
        button_layout.addStretch()
        
        # 结果区域布局
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.result_output)
        
        # 链接按钮布局
        link_layout = QHBoxLayout()
        link_layout.addStretch()
        link_layout.addWidget(self.open_link_btn)
        link_layout.addStretch()
        
        # 组合所有布局
        main_layout.addLayout(input_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(result_layout)
        main_layout.addLayout(link_layout)
        
        self.setLayout(main_layout)
    
    def generate_image(self):
        # 保存API密钥设置
        save_api = self.save_api_check.isChecked()
        self.settings.setValue("save_api", save_api)
        
        if save_api:
            self.settings.setValue("api_key", self.api_key_input.text())
        else:
            self.settings.remove("api_key")
        
        # 获取输入值
        prompt = self.prompt_input.toPlainText().strip()
        api_key = self.api_key_input.text().strip()
        model = self.model_combo.currentText().split(' ')[0]  # 提取模型名称
        
        # 验证输入
        if not prompt:
            QMessageBox.warning(self, '输入错误', '请输入绘图需求描述！')
            return
        if not api_key:
            QMessageBox.warning(self, '输入错误', '请输入API密钥！')
            return
        
        # 更新按钮状态
        self.generate_btn.setText('生成中...')
        self.generate_btn.setEnabled(False)
        QApplication.processEvents()  # 更新UI
        
        try:
            # 调用API
            client = ZhipuAI(api_key=api_key)
            response = client.images.generations(model=model, prompt=prompt)
            
            if response.data and response.data[0].url:
                image_url = response.data[0].url
                self.result_output.setText(f"图像生成成功！\nURL: {image_url}")
                self.current_url = image_url
                self.open_link_btn.setEnabled(True)
            else:
                self.result_output.setText("未获取到有效的图像URL，请检查API响应。")
                self.open_link_btn.setEnabled(False)
                
        except Exception as e:
            error_msg = f"生成图像时出错:\n{str(e)}"
            self.result_output.setText(error_msg)
            self.open_link_btn.setEnabled(False)
            QMessageBox.critical(self, 'API错误', error_msg)
        finally:
            # 恢复按钮状态
            self.generate_btn.setText('生成图像')
            self.generate_btn.setEnabled(True)
    
    def open_url(self):
        if hasattr(self, 'current_url') and self.current_url:
            QDesktopServices.openUrl(QUrl(self.current_url))
    
    def closeEvent(self, event):
        # 保存API密钥设置
        save_api = self.save_api_check.isChecked()
        self.settings.setValue("save_api", save_api)
        
        if save_api:
            self.settings.setValue("api_key", self.api_key_input.text())
        else:
            self.settings.remove("api_key")
        
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式
    
    # 设置应用样式
    app.setStyleSheet("""
        QWidget {
            background-color: #F5F5F5;
            font-family: Arial;
        }
        QLabel {
            color: #333333;
        }
        QLineEdit, QTextEdit, QComboBox {
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
        QTextEdit {
            background-color: #f8f8f8;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
    """)
    
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())
