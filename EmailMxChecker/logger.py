import logging
import weakref

class Logger:
	'''
	Cashed logger: associate a single logger instance with a given name
	'''

	_logger_cache = weakref.WeakValueDictionary()
	def __init__(self, name='logger', level=logging.DEBUG, handlers=['stream'], filename='app.log'):
		
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)

		logger_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		
		for handler in handlers:
			if handler == 'file':

				f_handler = logging.FileHandler(f'{filename}')
				f_handler.setFormatter(logger_format)
				self.logger.addHandler(f_handler)

			elif handler == 'stream':
				s_handler = logging.StreamHandler()
				s_handler.setFormatter(logger_format)
				self.logger.addHandler(s_handler)

			else:
				raise Exception('No handler specified')

	def __new__(cls, name='logger', level=logging.DEBUG, handlers=['stream'], filename='app.log'):
		if name in cls._logger_cache:
			return cls._logger_cache[name]
		else:
			self = super().__new__(cls)
			cls._logger_cache[name] = self
			return self

	def debug(self, msg):
	    self.logger.debug(msg)

	def info(self, msg):
	    self.logger.info(msg)

	def warning(self, msg):
	    self.logger.warning(msg)

	def error(self, msg):
	    self.logger.error(msg)
