import ansible_runner

r = ansible_runner.run(
    private_data_dir='/home/sszokoly/Projects/avansible/',      # See structure below
    playbook='/home/sszokoly/Projects/avansible/tasks/av-update-os__cm_lsp.yml',
    inventory='/home/sszokoly/Projects/avansible/lab_hosts.yml',                # Can be a path or inline content
    extravars={
        'src': '/home/sszokoly/Projects/avansible/staging/AV-CM10.1-RHEL8.4-SSP-031-01.tar.bz2',
        'dest': '/swlibrary'
    }
)

print("Status:", r.status)  # 'successful', 'failed', etc.
print("RC:", r.rc)
print("Stdout:", r.stdout.read())  # Or iterate over r.events