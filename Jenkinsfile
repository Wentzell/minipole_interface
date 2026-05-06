def projectName = "minipole_interface" /* set to app/repo name */

def dockerName = projectName.toLowerCase();
/* depend on triqs upstream branch/project */
def triqsBranch = env.CHANGE_TARGET ?: env.BRANCH_NAME
def triqsProject = '/TRIQS/triqs/' + triqsBranch.replaceAll('/', '%2F')
/* whether to keep and publish the results */
def keepInstall = !env.BRANCH_NAME.startsWith("PR-")

properties([
  disableConcurrentBuilds(),
  buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '30')),
  pipelineTriggers(keepInstall ? [
    upstream(
      threshold: 'SUCCESS',
      upstreamProjects: triqsProject
    )
  ] : [])
])

/* map of all builds to run, populated below */
def platforms = [:]

/****************** linux builds (in docker) */
/* Each platform must have a corresponding Dockerfile.PLATFORM in triqs/packaging */
def dockerPlatforms = ["ubuntu-clang", "ubuntu-gcc"]
/* .each is currently broken in jenkins */
for (int i = 0; i < dockerPlatforms.size(); i++) {
  def platform = dockerPlatforms[i]
  platforms[platform] = { -> node('linux && docker && triqs') {
    stage(platform) { timeout(time: 1, unit: 'HOURS') { ansiColor('xterm') {
      checkout scm
      /* construct a Dockerfile for this base */
      sh """
      ( echo "FROM flatironjenkins/triqs:${triqsBranch}-${env.STAGE_NAME}" ; sed '0,/^FROM /d' Dockerfile ) > Dockerfile.${env.STAGE_NAME}
        cp -f Dockerfile.${env.STAGE_NAME} Dockerfile
      """
      archiveArtifacts(artifacts: "Dockerfile.${env.STAGE_NAME}")
      /* build and tag */
      def img = docker.build("flatironjenkins/${dockerName}:${env.BRANCH_NAME}-${env.STAGE_NAME}", "--build-arg APPNAME=${projectName} --build-arg BUILD_ID=${env.BUILD_TAG} .")
      catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
        img.inside("--shm-size=4gb") {
          sh "cd \$SRC/${projectName} && pytest test/python -v"
        }
      }
      if (!keepInstall) {
        sh "docker rmi --no-prune ${img.imageName()}"
      }
    } } }
  } }
}

/****************** osx builds (on host) */
def osxPlatforms = [
  ["gcc", ['CC=gcc-15', 'CXX=g++-15', 'FC=gfortran-15']],
  ["clang", ['CC=$BREW/opt/llvm/bin/clang', 'CXX=$BREW/opt/llvm/bin/clang++', 'FC=gfortran-15', 'CXXFLAGS=-I$BREW/opt/llvm/include', 'LDFLAGS=-L$BREW/opt/llvm/lib']]
]
for (int i = 0; i < osxPlatforms.size(); i++) {
  def platformEnv = osxPlatforms[i]
  def platform = platformEnv[0]
  platforms["osx-$platform"] = { -> node('osx && triqs') {
    stage("osx-$platform") { timeout(time: 1, unit: 'HOURS') { ansiColor('xterm') {
      def srcDir = pwd()
      def triqsDir = "${env.HOME}/install/triqs/${triqsBranch}/${platform}"
      def venv = triqsDir

      checkout scm

      def hdf5 = "${env.BREW}/opt/hdf5"
      dir(srcDir) { withEnv(platformEnv[1].collect { it.replace('\$BREW', env.BREW) } + [
          "PATH=$venv/bin:${env.BREW}/bin:/usr/bin:/bin:/usr/sbin",
          "HDF5_ROOT=$hdf5",
          "C_INCLUDE_PATH=$hdf5/include:${env.BREW}/include",
          "CPLUS_INCLUDE_PATH=$venv/include:$hdf5/include:${env.BREW}/include",
          "LIBRARY_PATH=$venv/lib:$hdf5/lib:${env.BREW}/lib",
          "DYLD_LIBRARY_PATH=$venv/lib:$hdf5/lib:${env.BREW}/lib",
          "PYTHONPATH=$venv/lib/python3.13/site-packages",
          "CMAKE_PREFIX_PATH=$venv/lib/cmake/triqs",
          "VIRTUAL_ENV=$venv",
          "OMP_NUM_THREADS=2"]) {
        /* note: this is installing into the parent (triqs) venv, which is thus shared among apps and so not be completely safe */
        sh "pip3 install -U -e \".[test]\""
        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
          sh "pytest test/python -v"
        }
      } }
    } } }
  } }
}

/****************** wrap-up */
def error = null
try {
  parallel platforms
  if (keepInstall) { node('linux && docker && triqs') {
    /* Publish results */
    stage("publish") { timeout(time: 5, unit: 'MINUTES') {
      def commit = sh(returnStdout: true, script: "git rev-parse HEAD").trim()
      def release = env.BRANCH_NAME == "master" || env.BRANCH_NAME == "unstable" || sh(returnStdout: true, script: "git describe --exact-match HEAD || true").trim()
      def workDir = pwd(tmp:true)
      lock('triqs_publish') {
      /* Documentation is now published via .github/workflows/build_doc.yml. */
      /* Update packaging repo submodule */
      if (release) { dir("$workDir/packaging") { try {
        git(url: "ssh://git@github.com/TRIQS/packaging.git", branch: env.BRANCH_NAME, credentialsId: "ssh", changelog: false)
        // note: credentials used above don't work (need JENKINS-28335)
        sh """#!/bin/bash -ex
          dir="${projectName}"
          [[ -d triqs_\$dir ]] && dir=triqs_\$dir || [[ -d \$dir ]]
          echo "160000 commit ${commit}\t\$dir" | git update-index --index-info
          git commit --author='Flatiron Jenkins <jenkins@flatironinstitute.org>' -m 'Autoupdate ${projectName}' -m '${env.BUILD_TAG}'
          git push origin ${env.BRANCH_NAME}
        """
      } catch (err) {
        /* Ignore, non-critical -- might not exist on this branch */
        echo "Failed to update packaging repo"
      } } }
      }
    } }
  } }
} catch (err) {
  error = err
} finally {
  /* send email on build failure (declarative pipeline's post section would work better) */
  if ((error != null || currentBuild.currentResult != 'SUCCESS') && env.BRANCH_NAME != "jenkins") emailext(
    subject: "\$PROJECT_NAME - Build # \$BUILD_NUMBER - FAILED",
    body: """\$PROJECT_NAME - Build # \$BUILD_NUMBER - FAILED

Check console output at \$BUILD_URL to view full results.

Building \$BRANCH_NAME for \$CAUSE
\$JOB_DESCRIPTION

Changes:
\$CHANGES

End of build log:
\${BUILD_LOG,maxLines=60}
    """,
    to: 'nwentzell@flatironinstitute.org',
    recipientProviders: [
      [$class: 'DevelopersRecipientProvider'],
    ],
    replyTo: '$DEFAULT_REPLYTO'
  )
  if (error != null) throw error
}
