Feature: Create user, project, network via python-novaclient CLI
    Register and upload images, upload key-pair and start instances using euca2ools


    Scenario: Start instances using euca2ools

        Create admin user "{{user.name}}"
        Check user "{{user.name}}" exist

        Create project "{{project.name}}" for user "{{user.name}}"
        Check project "{{project.name}}" exist for user "{{user.name}}"

        Create network "{{network.cidr}}" with "{{network.nets}}" nets, "{{network.ips}}" ips per network
        Check network "{{network.cidr}}" exist

        Get novarc for project "{{project.name}}", user "{{user.name}}"

        Upload images from archive "{{image.path}}" using project "{{project.name}}", user "{{user.name}}" with bundle "{{bundle.image1}}"
        Check images with bundle "{{bundle.image1}}" exist

        Upload images from archive "{{image.path}}" using project "{{project.name}}", user "{{user.name}}" with bundle "{{bundle.image2}}"
        Check images with bundle "{{bundle.image2}}" exist

        Add keypair "{{keypair.name}}"
        Check keypair "{{keypair.name}}" exist

        Start instance "{{instance1}}" using image "{{bundle.image1}}" with key "{{keypair.name}}" VM type "{{vm_type}}" in group "default"
        Check instance "{{instance1}}" started
        Show instances

        Start instance "{{instance2}}" using image "{{bundle.image2}}" with key "{{keypair.name}}" VM type "{{vm_type}}" in group "default"
        Check instance "{{instance2}}" started
        Show instances
