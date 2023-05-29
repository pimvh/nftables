import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_nft_present(host):
    """test that the nft binary is present on the system"""

    assert host.run("which nft").rc == 0


def test_nft_tables_present(host):
    """test that the nft firewall table has been created"""

    with host.sudo():
        output = host.check_output("nft list tables")

    assert "inet firewall" in output
    assert "inet blocklist" in output


def nftables_abuseip_service(host):
    """test that the correct table files are created"""

    assert host.file("/usr/local/bin/manage_nft_abuseip_blocklist.py")
    assert host.service("update-abuseip-blocklist.timer").is_running
    assert host.service("update-abuseip-blocklist.timer").is_enabled


def test_table_files_created(host):
    """test that the correct table files are created"""

    with host.sudo():
        assert host.file("/etc/nftables/firewall.nft")
        assert host.file("/etc/nftables/defines.nft")
