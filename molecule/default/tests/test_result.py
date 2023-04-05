import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_nft_present(host):
    """test ssh ssh_known_hosts file has been created,
    with the requested key types"""

    assert host.run("which nft").rc == 0
