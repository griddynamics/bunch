Feature: Stop services, remove packages and clear all openstack stuff

    Scenario: Stop openstack services, delete database
        Delete database "nova"
        Delete user "nova"
        Stop services:
                         | ServiceName |
                        {% for service in openstack-services %}
                         | {{ service }} |
                        {% endfor %}
                        {% for service in supplementary-services %}
                         | {{ service }} |
                        {% endfor %}


    Scenario: Clear openstack RPMs
        Remove:
             """
                {% for package in packages-to-clean %}
                {{ package }} 
                {% endfor %}
            """


    Scenario: Clear openstack, mysql, glance state
        Delete state files


