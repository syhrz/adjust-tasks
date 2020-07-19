# Task02 -- WIP

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

So I search for E7-4830 in result it is a 8 cores cpu with 16 threads ([source](https://ark.intel.com/content/www/us/en/ark/products/53676/intel-xeon-processor-e7-4830-24m-cache-2-13-ghz-6-40-gt-s-intel-qpi.html)). So in total We will have 48 cores CPU with 96 threds. So the full specs are:

- 48 Cores / 96 threads CPU.
- 64GB of RAM.
- 2 TB of HDD
- 2x10Gbit Network

I would like to understand better on how SSL offloading affect performance. So at first I will create a virtual machine with 1/8 of the server capacity and load test it with around 1/8 of RPS = 3125 rps and see the vm metrics.

## Implementation

I'm using a few tools:
- Vagrant
- Ansible

With linux as working environment
```bash
uname -a                                                                                                                                                       Linux endurance 5.7.9-arch1-1 #1 SMP PREEMPT Thu, 16 Jul 2020 19:34:49 +0000 x86_64 GNU/Linux
```

First

```bash
vagrant init ubuntu/xenial64
```

Configure the cpu and memory
```ruby
  vb.memory = 8192
  vb.cpus = 6
```

And add steps to install nginx
```bash
  apt-get update
  apt-get install -y nginx
```

Then do SSH to vagrant to do a bit configuration.

```bash
vagrant ssh
```
