```python
git init
dvc init
```

#### Tracking data
```python
dvc add data/data.xml
```

#### Storage 
```python
mkdir %TEMP%/dvcstore
dvc remote add -d myremote %TEMP%\dvcstore
```

DVC supports many remote [storage types](https://dvc.org/doc/user-guide/data-management/remote-storage#supported-storage-types), including Amazon S3, NFS, SSH, Google Drive, Azure Blob Storage, and HDFS.

An example for a common use case is configuring an [Amazon S3](https://dvc.org/doc/user-guide/data-management/remote-storage/amazon-s3) remote:
```cli
dvc remote add -d storage s3://mybucket/dvcstore
```

#### Uploading data
```python
dvc push
```

#### DVC.yaml
```yaml
stages:
  prepare:
    cmd: python src/prepare.py data/data.xml
    deps:
      - src/prepare.py
      - data/data.xml
    params:
      - prepare.seed
      - prepare.split
    outs:
      - data/prepared
```

```python
dvc repro
dvc dag
```

## Summary

DVC pipelines ([`dvc.yaml`](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files) file, [`dvc stage add`](https://dvc.org/doc/command-reference/stage/add), and [`dvc repro`](https://dvc.org/doc/command-reference/repro) commands) solve a few important problems:

- _Automation_: run a sequence of steps in a "smart" way which makes iterating on your project faster. DVC automatically determines which parts of a project need to be run, and it caches "runs" and their results to avoid unnecessary reruns.
- _Reproducibility_: [`dvc.yaml`](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files) and [`dvc.lock`](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files#dvclock-file) files describe what data to use and which commands will generate the pipeline results (such as an ML model). Storing these files in Git makes it easy to version and share.

#### View metrics
```python
dvc metrics show
dvc plots show
```

#### CI/CD
#### Setup workflow
Go to .github/workflows/deploy-model-template.yml
```yml
on:
  # the workflow is triggered whenever a tag is pushed to the repository
  push:
    tags:
      - '*'
```
This means that the workflow will be triggered whenever we run model registry actions.