# Amazon ECS Fargate

# Table of Contents

- [Objective](#objective)
- [Diagram](#diagram)
- [Requirements](#requirements)
- [Caveats](#caveats)
- [Creation](#creation)
  * [Resources provisioned](#resources-provisioned)
  * [PoC](#poc)
- [Clean Up](#clean-up)

## Objective

Create a `CI/CD` pipeline serverless architecture with `AWS` managed services to deploy a sample `Python` application on `ECS Fargate`

## Diagram

![digram](img/diagram.png)

1. Updates are made to the `CodeCommit` repository
2. Automatically triggers the `CodeBuild` project
3. The project creates a `Docker` image in `Elastic Container Registry`
4. After the image is created `CodePipeline` triggers the deploy to `ECS Fargate`

## Requirements

- `AWS CLI` installed: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

- Export `AWS ACCESS KEY` and `AWS SECRET KEY` as environment variables:

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
```

- Configure an `SSH key` in your `IAM` credentials:

![ssh.png](img/ssh.png)

- `Python` library for AWS: [boto3](https://pypi.org/project/boto3/). 

## Caveats

Due to issues with Ansible module `ecs_taskdefiniton` I'm using the `AWS CLI` command to `register` the task definiton and a `python script` to deregister all task definitions in `roles/fargate/tasks/main.yml`.

## Creation

- Create the `CI/CD` pipeline with the following command:

`ansible-playbook -i inventory cicd-fargate-pipeline.yml --tags create_fargate`

### Resources provisioned

- `CodeCommit` repository for source code.
- `Elastic Container Registry` for `Docker` images.
- `CodeBuild` project to create the `Docker` image.
- `IAM Roles and Policies` for `CodeBuild`, `CodePipeline`, and `ECS Fargate`.
- `ECS Cluster`, `ECS Service`, and `ECS Fargate Task Definition`.
- `CodePipeline` to orchestrate the pipeline.

### PoC

- Clone the repository with the following command:

`git clone ssh://git-codecommit.us-west-2.amazonaws.com/v1/repos/python-sample-app`

- Copy the `source` code to the cloned repository:

`cp ../python-sample-code/* python-sample-app`

- `Push` the code the the `CodeCommit` repository:

```bash
cd python-sample-app
git add .
git commit -m "initial commit"
git push
```

- Open the `AWS CodePipeline` console to follow the execution steps:

[AWS CodePipeline console](https://us-west-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/python-sample-app-pipeline/view?region=us-west-2)

- At the end of the execution you should see a similar page:

![deploy_success](img/deploy_success.png)

- Open the `AWS ECS` console to retrieve the `public IP` assigned for the `task`: 

**Note:** It's possible to configure an `Application Load Balancer` and use it in conjunction with `ECS` in order to have a static endpoint. In this `PoC` it was not used in order to reduce the costs.

[AWS ECS console](https://us-west-2.console.aws.amazon.com/ecs/home?region=us-west-2#/clusters)

![public_ip](img/public_ip.png)

- Copy and paste the IP in the browser using the port `8080` and you should see the `Hello World` message:

![hello_world](img/hello_world.png)

## Clean Up

- Destroy the `CI/CD` pipeline with the following command:

`ansible-playbook -i inventory cicd-fargate-pipeline.yml --tags destroy_fargate`
