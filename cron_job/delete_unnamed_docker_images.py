#!/usr/bin/env python3

# This code finds unnamed Docker images and if they are not linked to user named images, then delete the unnamed Docker images.
import re
import subprocess

def send(cmd=[]):
    console_output = []
    cmd_result  = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    if cmd_result.returncode == 0:
       console_output = cmd_result.stdout.split("\n")
    return console_output

def print_console_output(console_output=[]):
    for line in console_output:
        print(f"{line}")

def docker_images():
    docker_images = {}
    ws = send(["docker", "images"])
    xs = (ws[1:])
    ys = xs[:len(xs)-1]
    zs = map(lambda y: re.split('  +', y), ys)
    docker_images = list(map(lambda z: {'repo': z[0], 'tag': z[1], 'id': z[2], 'created': z[3], 'size': z[4]}, zs))
    return docker_images

def named_unname_images():
    named_unname_images = {"unnamed": [], "named": []}
    regexp = re.compile(r'\.|/')
    images = docker_images()
    # None user named repos have 40 characteris length and does not have . or / in the name or is named <none>
    for image in images:
        if not bool(regexp.search(image["repo"])) and (len(image["repo"]) == 40 or "<none>" in image["repo"]):
            named_unname_images["unnamed"].append(image)
        else:
            named_unname_images["named"].append(image)
    return named_unname_images

def image_ids():
    images = named_unname_images()
    unnamed_images = images["unnamed"]
    named_images = images["named"]
    unnamed_image_ids = set(map(lambda image: image["id"], unnamed_images))
    named_image_ids = set(map(lambda image: image["id"], named_images))
    return {"unnamed_ids": unnamed_image_ids, "named_ids": named_image_ids}

def unnamed_images_to_delete():
    delete_these = []
    ids = image_ids()
    for id in ids["unnamed_ids"]:
        if id not in ids["named_ids"]:
            delete_these.append(id)
    return delete_these

def delete_unnamed_images():
    images = unnamed_images_to_delete()
    for image in images:
        send(["docker","rmi","-f", image])

def main():
    delete_unnamed_images()