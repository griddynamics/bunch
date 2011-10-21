Feature: Install, initialize test enviroment, run instances
    Start services, create database, user, project, network

    Scenario: Install Openstack RPM
        Install "{{nova.rpm_packages}}"
        Check if "{{nova.rpm_packages}}" is installed
        Change flags in "{{nova.conf_file}}":
                         | Flag                      | Value                                 |
                         | --verbose                 | true                                  |
                         | --vlan_interface          | eth0                                  |
                         | --sql_connection          | mysql://nova:nova@127.0.0.1/nova      |
                         | --ec2_url                 | http://{{ myip }}:8773/services/Cloud |
                         | --s3_host                 | {{ myip }}                            |
                         | --cc_host                 | {{ myip }}                            |
                         | --rabbit_host             | {{ myip }}                            |
                         | --sql_connection          | mysql://nova:nova@{{ myip}}/nova      |
                         | --glance_api_servers      | {{ myip}}:9292                        |

    
    Scenario: Start supplementary services
        Start services:
                         | ServiceName     |
                        {% for service in supplementary-services %}
                         | {{ service }} |
                        {% endfor %}

        Check services running:
                         | ServiceName     |
                        {% for service in supplementary-services %}
                         | {{ service }} |
                        {% endfor %}


    Scenario: Setup MySQL
        Create database "{{db.db_name}}" with data "cfg/init.sql"
        Check database "{{db.db_name}}" exists
        Sync database


    Scenario: Start OpenStack services
        Start services:
                         | ServiceName |
                        {% for service in openstack-services %}
                         | {{ service }} |
                        {% endfor %}

        Check services running:
                         | ServiceName |
                        {% for service in openstack-services %}
                         | {{ service }} |
                        {% endfor %}

