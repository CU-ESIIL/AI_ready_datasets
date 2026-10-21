"""Inspected external capabilities; metadata only, no CubeDynamics import or code copy."""
VERSION='0.1.0rc3'
# Adapter glue through public apply is explicitly distinguished from dedicated verbs.
SPECS={
 'cubedynamics.select': ('Select one documented variable','verbs.apply (fixed xarray variable/band selection)',{'variable_ref':{'const':'request.variable'}},False,False,False),
 'cubedynamics.subset': ('Select a bounded time/y/x window','verbs.apply (fixed xarray isel)',{'window_ref':{'const':'request.window'}},False,False,False),
 'cubedynamics.month_filter': ('Select documented calendar months','verbs.month_filter',{'months_ref':{'const':'request.months'}},False,False,False),
 'cubedynamics.quality_mask': ('Apply an explicit aligned quality predicate','verbs.apply (fixed xarray where/isin)',{'mask_ref':{'const':'inputs.quality'},'classes_ref':{'const':'request.allowed_quality_classes'}},True,False,False),
 'cubedynamics.temporal_mean': ('Mean over complete equal-duration intervals','verbs.mean',{'statistic':{'const':'mean'},'support_ref':{'const':'request.target_temporal_support'}},True,False,True),
 'cubedynamics.align_time': ('Validate exact labels and known equal temporal support','verbs.align_time',{'target_ref':{'const':'inputs.reference'},'mode':{'const':'require_exact_support'}},False,False,False),
 'cubedynamics.align_nearest': ('Same-CRS nearest spatial sampling; exact time only','verbs.align_cube',{'target_ref':{'const':'inputs.reference'},'method':{'const':'nearest'}},True,True,False),
}

def definitions():
    return [dict(operation_id=identifier,legacy_name=identifier,name=name,description=name,
        backend='cubedynamics',backend_version=VERSION,upstream_api=api,
        input_contract='xarray DataArray/Dataset, explicit time/y/x coordinates, optional band, bound metadata',
        output_contract='xarray object plus TransformationResult; no automatic semantic equivalence',
        parameter_schema={'type':'object','additionalProperties':False,'properties':parameters,'required':list(parameters)},
        implementation_reference='dataset_prototype.cubedynamics_backend.CubeDynamicsBackend.execute',
        scientific_assumptions=('Computational feasibility is not scientific validity.',
            'Mean is unweighted and requires complete equal-duration interval evidence.' if temporal else 'No implicit CRS transformation or biological equivalence.'),
        preconditions=('exact-recipe human decision','source/context digest and scientific metadata verified','bounded input/output graph'),
        postconditions=('shape, units, CRS and support changes recorded','lazy values stay lazy unless explicitly materialized'),
        changes_values=values,changes_spatial_support=spatial,changes_spatial_resolution=spatial,
        changes_temporal_support=temporal,changes_temporal_resolution=temporal,
        changes_extent=identifier in {'cubedynamics.subset','cubedynamics.month_filter'},
        requires_human_approval=True,lazy_or_eager='LAZY / BATCHED; explicit bounded materialization only',
        tests=('tests/test_cubedynamics.py',),
        provenance='external package/dependency versions, upstream API, trace, source/recipe/review and window evidence')
        for identifier,(name,api,parameters,values,spatial,temporal) in SPECS.items()]
