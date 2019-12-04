import typing

from core.base.SuperManager import SuperManager
from core.util.model.Logger import Logger


class _ProjectAliceException(Exception):

	def __init__(self, message: str = None, status: int = None, context: list = None):
		self._logger = Logger()
		self._message = message
		self._status = status
		self._context = context
		super().__init__(message)


	@property
	def message(self) -> str:
		return self._message


	@property
	def status(self) -> typing.Optional[int]:
		return self._status


	@property
	def context(self) -> typing.Optional[list]:
		return self._context


class SamkillaException(_ProjectAliceException):
	def __init__(self, status: int, message: str, context: list):
		super().__init__(message, status, context)


class FunctionNotImplemented(_ProjectAliceException):
	def __init__(self, clazz: str, funcName: str):
		self._logger.logError(f'{funcName} must be implemented in {clazz}!')


class ModuleStartingFailed(_ProjectAliceException):
	def __init__(self, moduleName: str = '', error: str = ''):
		super().__init__(message=error)
		self._logger.logInfo(f'An error occured while starting a module: {error}')

		if moduleName:
			SuperManager.getInstance().moduleManager.deactivateModule(moduleName)


class ModuleStartDelayed(_ProjectAliceException):
	def __init__(self, moduleName):
		super().__init__(moduleName)
		self._logger.logWarning('Delaying module start')
		SuperManager.getInstance().moduleManager.getModuleInstance(moduleName).delayed = True


class IntentError(_ProjectAliceException):
	def __init__(self, status: int, message: str, context: list):
		super().__init__(message, status, context)


class HttpError(_ProjectAliceException):
	def __init__(self, status: int, message: str, context: list):
		super().__init__(message, status, context)


class IntentWithUnknownSlotError(_ProjectAliceException):
	def __init__(self, status: int, message: str, context: list):
		super().__init__(message, status, context)


class AssistantNotFoundError(_ProjectAliceException):
	def __init__(self, status: int, message: str, context: list):
		super().__init__(message, status, context)


class ModuleNotConditionCompliant(_ProjectAliceException):
	def __init__(self, message: str, moduleName: str, condition: str, conditionValue: str):
		self._moduleName = moduleName
		self._condition = condition
		self._conditionValue = conditionValue
		super().__init__(message)


	@property
	def moduleName(self) -> str:
		return self._moduleName


	@property
	def condition(self) -> str:
		return self._condition


	@property
	def conditionValue(self) -> str:
		return self._conditionValue


class OfflineError(_ProjectAliceException): pass
class DbConnectionError(_ProjectAliceException): pass
class InvalidQuery(_ProjectAliceException): pass
class AccessLevelTooLow(_ProjectAliceException): pass
class GithubTokenFailed(_ProjectAliceException): pass
class GithubRateLimit(_ProjectAliceException): pass
class GithubNotFound(_ProjectAliceException): pass
class LanguageManagerLangNotSupported(_ProjectAliceException): pass
class ConfigurationUpdateFailed(_ProjectAliceException): pass

class VitalConfigMissing(_ProjectAliceException):
	def __init__(self, message: str = None):
		super().__init__(message)
		self._logger.logWarning(f'A vital configuration ("{message}") is missing. Make sure the following configurations are set: {" / ".join(SuperManager.getInstance().configManager.vitalConfigs)}')
		SuperManager.getInstance().projectAlice.onStop()
