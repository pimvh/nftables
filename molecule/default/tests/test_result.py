import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_nft_present(host):
    """test ssh ssh_known_hosts file has been created,
    with the requested key types"""

    assert host.run("which nft").rc == 0


def test_nft_table_firewall(host):
    """test ssh ssh_known_hosts file has been created,
    with the requested key types"""

    assert host.run("nft list tables").contains("inet firewall")


def nftables_abuseip_service(host):
    """test that the correct table files are created"""

    assert host.file("/usr/local/bin/manage_nft_abuseip_blocklist.py")
    assert host.service("update-abuseip-blocklist.timer").is_running


def test_table_files_created(host):
    """test that the correct table files are created"""

    with host.sudo():
        assert host.file("/etc/nftables/firewall.nft")
        assert host.file("/etc/nftables/defines.nft")
