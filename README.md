# JIRA integration pack

This pack consists of a sample JIRA sensor and a JIRA action.

## Installation

You will need to have `gcc` installed on your system. For Ubuntu systems, run `sudo apt-get install gcc`. For Redhat/CentOS
systems, run `sudo yum install gcc libffi-devel python-devel openssl-devel`. To build the python cryptography dependency (part of the following `st2 pack install` command) 2GB of RAM is recommended. In some cases adding a swap file may eliminate strange gcc compiler errors.

Then install this pack with: `st2 pack install jira`

## Configuration

Copy the example configuration in [jira.yaml.example](./jira.yaml.example)
to `/opt/stackstorm/configs/jira.yaml` and edit as required.

* ``url`` - URL of the JIRA instance (e.g. ``https://myproject.atlassian.net``)
* ``poll_interval`` - Polling interval - default 30s
* ``project`` - Key of the project which will be used as a default with some of the actions which
  don't require or allow you to specify a project (e.g. ``STORM``).
* ``verify`` - Verify SSL certificates. Default True. Set to False to disable verification
* ``auth_method`` - Specify either `basic` or `oauth` authentication

Include the following settings when using the `oauth` auth_method:
* ``rsa_cert_file`` - Path to the file with a private key
* ``oauth_token`` - OAuth token
* ``oauth_secret`` - OAuth secret
* ``consumer_key`` - Consumer key

Include the following settings when using the `basic` auth_method:
* ``username`` - Username
* ``password`` - Password

If using the `oauth` auth_method, take a look at the OAuth section below for further setup instructions.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

### OAuth

### Disclaimer

This documentation is written as of 06/17/2014. JIRA 6.3 implements OAuth1. Most of this doc would need to be revised when JIRA switches to OAuth2.

### Steps

1. Generate RSA public/private key pair
    ```
    # This will create a 2048 length RSA private key
    $openssl genrsa -out mykey.pem 2048
    ```

    ```
    # Now, create the public key associated with that private key
    openssl rsa -in mykey.pem -pubout
    ```
2. Generate a consumer key. You can use python uuid.uuid4() to do this, for example:

    ```
    $ python
    Python 2.7.10 (default, Jul 30 2016, 19:40:32)
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import uuid
    >>> print uuid.uuid4()
    210660f1-ca8a-40d5-a6ee-295ccbf3074d
    >>>
    ```
    
3. Configure JIRA for external access:
     * Go to AppLinks section of your JIRA - https://JIRA_SERVER/plugins/servlet/applinks/listApplicationLinks
     * Create a Generic Application with some fake URL
     * Click Edit, hit IncomingAuthentication. Plug in the consumer key and RSA public key you generated.
4. Get access token using this [script](https://github.com/lakshmi-kannan/jira-oauth-access-token-generator/blob/master/generate_access_token.py). You may need to install additional libraries to run that script, and you
  will need to edit the script to use your file locations. Check the [README](https://github.com/lakshmi-kannan/jira-oauth-access-token-generator/blob/master/README.md) file for more information.
  The access token is printed at the end of running that script. Save these keys somewhere safe. 
5. Plug in the access token and access secret into the sensor or action. You are good to make JIRA calls. Note: OAuth token expires. You'll have to repeat the process based on the expiry date. 

## Sensors

### JiraSensor

The sensor monitors for new tickets and sends a trigger into the system whenever there is a new ticket.

## Actions

* ``create_issue`` - Action which creates a new JIRA issue.
* ``get_issue`` - Action which retrieves details for a particular issue.
