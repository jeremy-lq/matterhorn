import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import pynag.Model

# CONFIG = pynag.Model.config
# RESOURCES = CONFIG.get_resources()

class Host(object):
    def __init__(self, pynag_host):
        """
        :type pynag_host: pynag.Model.Host
        """
        self.pynag_host = pynag_host

    @classmethod
    def default_bernard_config(cls):
        return {
            'core': {
                'schedule': {
                    'timeout': 5,
                    'period': 60,
                    'attempts': 3,
                },
                'notification': '',
                'notify_startup': '',
            },
            'checks': [
            ]
        }

    def get_bernard_config(self):
        config = Host.default_bernard_config()

        if self.pynag_host.max_check_attempts:
            config['core']['schedule']['attempts'] = int(self.pynag_host.max_check_attempts)
        if self.pynag_host.check_interval:
            config['core']['schedule']['period'] = 60 * int(self.pynag_host.check_interval)

        notification = ''
        if self.pynag_host.get_effective_contact_groups():
            notification = '%s %s' % (notification, ' '.join(
                ['@%s' % cg.contactgroup_name for cg in self.pynag_host.get_effective_contact_groups()]))

        if self.pynag_host.get_effective_contacts():
            notification = '%s %s' % (notification, ' '.join(
                ['@%s' % (c.email or c.contact_name) for c in self.get_effective_contacts()]))


        # Check for host status
        # command = self.pynag_host.get_effective_command_line()
        # command = command.split()
        # if command:
        #     checks.append({
        #         'filename': command.pop(0),
        #         'args': command,
        #     })

        # Checks for services status
        for service in self.pynag_host.get_effective_services():
            check = {}
            assert isinstance(service, pynag.Model.Service)
            command = service.get_effective_command_line()
            command = command.split()
            filename = command.pop(0)
            args = ['"%s"' % c.replace('"', '\\"') for c in command]
            if command:
                check_config = {
                    'filename': command.pop(0),
                    'args': command,
                }
                if notification:
                    check_config['notification'] = notification.strip()
                config['checks'].append(check_config)

        return config


hosts = []
pynag_hosts = pynag.Model.Host.objects.all

for pynag_host in pynag_hosts:
    host = Host(pynag_host)
    config_file = open('/tmp/bernard_config_%s' % host.pynag_host.host_name, 'w')
    config = host.get_bernard_config()
    yaml.dump(config, config_file)
    config_file.close()

