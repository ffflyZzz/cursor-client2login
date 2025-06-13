#!/usr/bin/env python3
import json
import sys
import struct
import sqlite3
import os
import platform
import stat
from typing import Dict, Any, Optional, Callable
from abc import ABC, abstractmethod


class BaseActionHandler(ABC):
    """Action处理器基类"""
    
    @abstractmethod
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求并返回响应"""
        pass


class CursorDataManager:
    """Cursor数据管理器"""

    @staticmethod
    def get_cursor_db_path() -> str:
        """根据操作系统获取Cursor数据库路径"""
        system = platform.system()

        if system == "Windows":
            appdata = os.getenv("APPDATA")
            if appdata is None:
                raise EnvironmentError("APPDATA 环境变量未设置")
            return os.path.join(appdata, "Cursor", "User", "globalStorage", "state.vscdb")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/state.vscdb")
        elif system == "Linux":
            return os.path.expanduser("~/.config/Cursor/User/globalStorage/state.vscdb")
        else:
            raise NotImplementedError(f"不支持的操作系统: {system}")

    @staticmethod
    def check_file_permissions(file_path: str) -> Dict[str, Any]:
        """检查文件权限和可访问性"""
        try:
            if not os.path.exists(file_path):
                return {
                    "accessible": False,
                    "error": f"文件不存在: {file_path}",
                    "suggestions": [
                        "确保Cursor已安装并至少运行过一次",
                        "检查Cursor是否已登录过账户",
                        "验证文件路径是否正确"
                    ]
                }

            # 检查文件权限
            file_stat = os.stat(file_path)
            file_mode = file_stat.st_mode

            # 检查读权限
            if not os.access(file_path, os.R_OK):
                return {
                    "accessible": False,
                    "error": f"文件无读取权限: {file_path}",
                    "file_mode": oct(file_mode),
                    "suggestions": [
                        f"尝试修改文件权限: chmod 644 '{file_path}'",
                        "检查文件是否被其他程序占用",
                        "以管理员权限运行程序"
                    ]
                }

            # 检查文件大小
            file_size = file_stat.st_size
            if file_size == 0:
                return {
                    "accessible": False,
                    "error": f"文件为空: {file_path}",
                    "suggestions": [
                        "重新启动Cursor应用程序",
                        "重新登录Cursor账户",
                        "检查Cursor是否正常工作"
                    ]
                }

            return {
                "accessible": True,
                "file_size": file_size,
                "file_mode": oct(file_mode),
                "last_modified": file_stat.st_mtime
            }

        except PermissionError as e:
            return {
                "accessible": False,
                "error": f"权限错误: {str(e)}",
                "suggestions": [
                    "以管理员权限运行程序",
                    "检查文件权限设置",
                    "确保当前用户有访问权限"
                ]
            }
        except Exception as e:
            return {
                "accessible": False,
                "error": f"检查文件权限时发生错误: {str(e)}",
                "suggestions": [
                    "检查文件路径是否正确",
                    "确保文件系统正常",
                    "重试操作"
                ]
            }

    @staticmethod
    def get_scope_json_path() -> str:
        """根据操作系统获取scope_v3.json路径"""
        system = platform.system()
        
        if system == "Windows":
            appdata = os.getenv("APPDATA")
            if appdata is None:
                raise EnvironmentError("APPDATA 环境变量未设置")
            return os.path.join(appdata, "Cursor", "sentry", "scope_v3.json")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/Cursor/sentry/scope_v3.json")
        elif system == "Linux":
            return os.path.expanduser("~/.config/Cursor/sentry/scope_v3.json")
        else:
            raise NotImplementedError(f"不支持的操作系统: {system}")

    @classmethod
    def read_access_token(cls) -> Dict[str, Any]:
        """从Cursor数据库读取accessToken"""
        try:
            db_path = cls.get_cursor_db_path()

            # 检查文件权限和可访问性
            permission_check = cls.check_file_permissions(db_path)
            if not permission_check["accessible"]:
                return {
                    "error": permission_check["error"],
                    "suggestions": permission_check.get("suggestions", []),
                    "file_path": db_path
                }

            # 尝试连接数据库
            conn = None
            try:
                conn = sqlite3.connect(db_path, timeout=10.0)
                conn.execute("PRAGMA journal_mode=WAL")  # 设置WAL模式以避免锁定问题
                cursor = conn.cursor()

                # 检查表是否存在
                cursor.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='itemTable'
                """)
                if not cursor.fetchone():
                    return {
                        "error": "数据库中未找到itemTable表",
                        "suggestions": [
                            "确保Cursor已正确安装并运行过",
                            "检查数据库文件是否完整",
                            "尝试重新启动Cursor应用"
                        ],
                        "file_path": db_path
                    }

                # 查询accessToken
                cursor.execute("SELECT value FROM itemTable WHERE key = ?", ("cursorAuth/accessToken",))
                result = cursor.fetchone()

                if result and result[0]:
                    return {"accessToken": result[0]}
                else:
                    return {
                        "error": "未找到accessToken或token为空",
                        "suggestions": [
                            "确保已在Cursor中登录账户",
                            "尝试重新登录Cursor",
                            "检查网络连接是否正常"
                        ],
                        "file_path": db_path
                    }

            except sqlite3.OperationalError as e:
                error_msg = str(e).lower()
                if "database is locked" in error_msg:
                    return {
                        "error": "数据库被锁定，可能Cursor正在运行",
                        "suggestions": [
                            "关闭Cursor应用程序后重试",
                            "等待几秒钟后重试",
                            "检查是否有其他程序在访问数据库"
                        ],
                        "file_path": db_path,
                        "technical_error": str(e)
                    }
                elif "no such table" in error_msg:
                    return {
                        "error": "数据库表结构异常",
                        "suggestions": [
                            "数据库可能已损坏，尝试重新安装Cursor",
                            "检查Cursor版本是否兼容",
                            "备份数据后重置Cursor配置"
                        ],
                        "file_path": db_path,
                        "technical_error": str(e)
                    }
                else:
                    return {
                        "error": f"数据库操作错误: {str(e)}",
                        "suggestions": [
                            "检查数据库文件是否损坏",
                            "尝试重新启动Cursor",
                            "检查磁盘空间是否充足"
                        ],
                        "file_path": db_path,
                        "technical_error": str(e)
                    }

            except sqlite3.DatabaseError as e:
                return {
                    "error": f"数据库错误: {str(e)}",
                    "suggestions": [
                        "数据库文件可能已损坏",
                        "尝试重新安装Cursor",
                        "检查文件系统是否正常"
                    ],
                    "file_path": db_path,
                    "technical_error": str(e)
                }

            finally:
                if conn:
                    try:
                        conn.close()
                    except Exception:
                        pass  # 忽略关闭连接时的错误

        except Exception as e:
            return {
                "error": f"读取accessToken时发生未预期错误: {str(e)}",
                "suggestions": [
                    "检查系统权限设置",
                    "确保Python有足够权限访问文件",
                    "重启系统后重试"
                ],
                "technical_error": str(e)
            }

    @classmethod
    def read_scope_json(cls) -> Dict[str, Any]:
        """读取scope_v3.json文件"""
        try:
            json_path = cls.get_scope_json_path()

            # 检查文件权限和可访问性
            permission_check = cls.check_file_permissions(json_path)
            if not permission_check["accessible"]:
                return {
                    "error": permission_check["error"],
                    "suggestions": permission_check.get("suggestions", []),
                    "file_path": json_path
                }

            # 尝试读取文件
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 检查文件内容是否为空
                if not content.strip():
                    return {
                        "error": "JSON文件内容为空",
                        "suggestions": [
                            "重新启动Cursor应用程序",
                            "重新登录Cursor账户",
                            "检查Cursor是否正常运行"
                        ],
                        "file_path": json_path
                    }

                # 移除末尾的%符号（如果存在）
                content = content.rstrip('%').strip()

                # 尝试解析JSON
                try:
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    return {
                        "error": f"JSON格式错误: {str(e)}",
                        "suggestions": [
                            "文件可能已损坏，尝试重新登录Cursor",
                            "检查文件是否被意外修改",
                            "重新启动Cursor应用程序"
                        ],
                        "file_path": json_path,
                        "technical_error": str(e)
                    }

                # 验证JSON结构
                if not isinstance(data, dict):
                    return {
                        "error": "JSON文件格式不正确，根元素应为对象",
                        "suggestions": [
                            "文件结构异常，尝试重新登录Cursor",
                            "检查Cursor版本是否兼容"
                        ],
                        "file_path": json_path
                    }

                # 提取email和userid
                scope_data = data.get("scope")
                if not scope_data or not isinstance(scope_data, dict):
                    return {
                        "error": "JSON文件中缺少scope字段或格式错误",
                        "suggestions": [
                            "确保已在Cursor中完成登录",
                            "尝试重新登录Cursor账户",
                            "检查账户状态是否正常"
                        ],
                        "file_path": json_path
                    }

                user_info = scope_data.get("user")
                if not user_info or not isinstance(user_info, dict):
                    return {
                        "error": "JSON文件中缺少用户信息或格式错误",
                        "suggestions": [
                            "确保已在Cursor中完成登录",
                            "检查账户信息是否完整",
                            "尝试重新登录Cursor账户"
                        ],
                        "file_path": json_path
                    }

                email = user_info.get("email")
                user_id_full = user_info.get("id")

                if not email:
                    return {
                        "error": "未找到邮箱信息",
                        "suggestions": [
                            "确保使用邮箱登录Cursor",
                            "检查账户信息是否完整",
                            "尝试重新登录"
                        ],
                        "file_path": json_path
                    }

                if not user_id_full or not isinstance(user_id_full, str) or "|" not in user_id_full:
                    return {
                        "error": "用户ID格式不正确或缺失",
                        "suggestions": [
                            "用户ID应包含'|'分隔符",
                            "尝试重新登录Cursor账户",
                            "检查账户状态是否正常"
                        ],
                        "file_path": json_path,
                        "found_id": user_id_full
                    }

                userid = user_id_full.split("|")[1]
                if not userid:
                    return {
                        "error": "无法从用户ID中提取有效的userid",
                        "suggestions": [
                            "用户ID格式异常",
                            "尝试重新登录Cursor账户"
                        ],
                        "file_path": json_path,
                        "found_id": user_id_full
                    }

                return {
                    "email": email,
                    "userid": userid
                }

            except PermissionError as e:
                return {
                    "error": f"文件权限错误: {str(e)}",
                    "suggestions": [
                        "以管理员权限运行程序",
                        "检查文件权限设置",
                        "确保当前用户有读取权限"
                    ],
                    "file_path": json_path,
                    "technical_error": str(e)
                }

            except IOError as e:
                return {
                    "error": f"文件读取错误: {str(e)}",
                    "suggestions": [
                        "检查磁盘空间是否充足",
                        "确保文件未被其他程序占用",
                        "检查文件系统是否正常"
                    ],
                    "file_path": json_path,
                    "technical_error": str(e)
                }

        except Exception as e:
            return {
                "error": f"读取scope_v3.json时发生未预期错误: {str(e)}",
                "suggestions": [
                    "检查系统权限设置",
                    "确保Python有足够权限访问文件",
                    "重启系统后重试"
                ],
                "technical_error": str(e)
            }


class GetAccessTokenHandler(BaseActionHandler):
    """获取AccessToken处理器"""

    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params参数保留用于未来扩展，当前不使用
        _ = params  # 显式标记参数已知但未使用
        return CursorDataManager.read_access_token()


class GetScopeDataHandler(BaseActionHandler):
    """获取Scope数据处理器"""

    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params参数保留用于未来扩展，当前不使用
        _ = params  # 显式标记参数已知但未使用
        return CursorDataManager.read_scope_json()


class GetClientCurrentDataHandler(BaseActionHandler):
    """获取客户端当前数据处理器"""

    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # params参数保留用于未来扩展，当前不使用
        _ = params  # 显式标记参数已知但未使用

        # 获取所有数据
        token_result = CursorDataManager.read_access_token()
        scope_result = CursorDataManager.read_scope_json()

        # 检查token获取结果
        if "error" in token_result:
            return {
                "error": f"获取AccessToken失败: {token_result['error']}",
                "suggestions": token_result.get("suggestions", []),
                "component": "accessToken",
                "details": token_result
            }

        # 检查scope获取结果
        if "error" in scope_result:
            return {
                "error": f"获取用户信息失败: {scope_result['error']}",
                "suggestions": scope_result.get("suggestions", []),
                "component": "scopeData",
                "details": scope_result
            }

        # 验证数据完整性
        access_token = token_result.get("accessToken")
        email = scope_result.get("email")
        userid = scope_result.get("userid")

        if not access_token:
            return {
                "error": "AccessToken为空",
                "suggestions": [
                    "确保已在Cursor中登录账户",
                    "尝试重新登录Cursor",
                    "检查网络连接是否正常"
                ],
                "component": "accessToken"
            }

        if not email:
            return {
                "error": "邮箱信息为空",
                "suggestions": [
                    "确保使用邮箱登录Cursor",
                    "检查账户信息是否完整"
                ],
                "component": "email"
            }

        if not userid:
            return {
                "error": "用户ID为空",
                "suggestions": [
                    "用户ID格式可能异常",
                    "尝试重新登录Cursor账户"
                ],
                "component": "userid"
            }

        return {
            "accessToken": access_token,
            "email": email,
            "userid": userid,
            "success": True
        }


class ActionRegistry:
    """Action注册表"""
    
    def __init__(self):
        self._handlers: Dict[str, BaseActionHandler] = {}
    
    def register(self, action: str, handler: BaseActionHandler) -> None:
        """注册action处理器"""
        self._handlers[action] = handler
    
    def get_handler(self, action: str) -> Optional[BaseActionHandler]:
        """获取action处理器"""
        return self._handlers.get(action)
    
    def get_available_actions(self) -> list:
        """获取所有可用的action"""
        return list(self._handlers.keys())


class NativeHostServer:
    """原生主机服务器"""
    
    def __init__(self):
        self.registry = ActionRegistry()
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认的处理器"""
        self.registry.register("getAccessToken", GetAccessTokenHandler())
        self.registry.register("getScopeData", GetScopeDataHandler())
        self.registry.register("getClientCurrentData", GetClientCurrentDataHandler())
    
    def add_handler(self, action: str, handler: BaseActionHandler) -> None:
        """添加新的action处理器"""
        self.registry.register(action, handler)
    
    @staticmethod
    def get_message() -> Dict[str, Any]:
        """从Chrome读取消息"""
        raw_length = sys.stdin.buffer.read(4)
        if len(raw_length) == 0:
            sys.exit(0)
        message_length = struct.unpack('@I', raw_length)[0]
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        return json.loads(message)
    
    @staticmethod
    def send_message(message: Dict[str, Any]) -> None:
        """发送消息到Chrome"""
        encoded_content = json.dumps(message).encode('utf-8')
        encoded_length = struct.pack('@I', len(encoded_content))
        sys.stdout.buffer.write(encoded_length)
        sys.stdout.buffer.write(encoded_content)
        sys.stdout.buffer.flush()
    
    def handle_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        action = message.get("action")
        params = message.get("params", {})
        
        if not action:
            return {"error": "缺少action参数"}
        
        handler = self.registry.get_handler(action)
        if not handler:
            available_actions = self.registry.get_available_actions()
            return {
                "error": f"未知操作: {action}",
                "available_actions": available_actions
            }
        
        try:
            return handler.handle(params)
        except Exception as e:
            return {"error": f"处理action '{action}' 时发生错误: {str(e)}"}
    
    def run(self) -> None:
        """运行服务器"""
        try:
            message = self.get_message()
            response = self.handle_request(message)
            self.send_message(response)
        except Exception as e:
            self.send_message({"error": f"处理请求时发生错误: {str(e)}"})


def main():
    """主函数"""
    server = NativeHostServer()
    server.run()


if __name__ == "__main__":
    main()