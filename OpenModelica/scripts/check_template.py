from jinja2 import Template

import config


def main():
    with open('translateModelFMU.mos.template', 'r') as fh:
        template_content = fh.read()

    template = Template(template_content)

    model_file = config.OPENMODELICA_MODELS_DIR / 'test.mo'
    build_dir = config.OPENMODELICA_BUILD_DIR
    model_name = 'test'
    fmu_name = config.OPENMODELICA_FMUS_DIR / 'test.fmu'

    # Convert paths to use forward slashes,
    # since omc does not like backward slashes in paths
    model_file = model_file.as_posix()
    build_dir = build_dir.as_posix()
    fmu_name = fmu_name.as_posix()

    output = template.render(
        model_file=model_file,
        build_dir=build_dir,
        model_name=model_name,
        fmu_name=fmu_name
    )

    print(output)


if __name__ == '__main__':
    main()
