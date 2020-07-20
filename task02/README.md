# Task02

## Task Description

Imagine a server with the following specs:

- 4 times Intel(R) Xeon(R) CPU E7-4830 v4 @ 2.00GHz
- 64GB of ram
- 2 tb HDD disk space
- 2 x 10Gbit/s nics

The server is used for SSL offloading and proxies around 25000 requests per second. Please let us know which metrics are interesting to monitor in that specific case and how would you do that?  What are the challenges of monitoring this?

## Thinking Process

A few things that still unknown that might help in understanding the metrics:
- Details of processor specification.
- Disk I/O speed not present, but seems like SSL offloading more CPU heavy we might not need it.
- OS and service (nginx / haproxy) configuration.

So I search for E7-4830 in result it is a 8 cores cpu with 16 threads ([source](https://ark.intel.com/content/www/us/en/ark/products/53676/intel-xeon-processor-e7-4830-24m-cache-2-13-ghz-6-40-gt-s-intel-qpi.html)). So in total We will have 48 cores CPU with 96 threds. So the full specs are:

- 48 Cores threads CPU.
- 64GB of RAM.
- 2 TB of HDD
- 2x10Gbit Network

From my point of view some *performance* metrics that are very interesting to monitor are:
- Latency.
- Time per request and
- Number of failed requests.

The challenges will be how to find the bottlenecks in the system that will handle 25k rps.

## Implementation

I'm using a few tools:
- Vagrant.
- Ansible for easier configuration management.

I currently run the setup With linux as working environment.
```bash
uname -a
Linux endurance 5.7.9-arch1-1 #1 SMP PREEMPT Thu, 16 Jul 2020 19:34:49 +0000 x86_64 GNU/Linux
```

First initialize Vagrantfile.
```bash
vagrant init ubuntu/xenial64
```

Configure the cpu and memory of the virtual machine by modifying these value in Vagrantfile.
```ruby
  vb.memory = 8192
  vb.cpus = 6
```

And add steps to install nginx in the Vagrantfile.
```bash
  apt-get update
  apt-get install -y nginx
```

Then do SSH to vagrant to do a bit configuration.
```bash
vagrant ssh
```
